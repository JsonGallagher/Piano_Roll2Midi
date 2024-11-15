import os
import base64
import openai
from midiutil import MIDIFile
from PIL import Image
import json
from typing import List, Dict, Tuple, Optional

class PianoRollInterpreter:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        print(f"Initializing with API key: {api_key[:4]}...")  # Show first 4 chars only
        self.api_key = api_key
        openai.api_key = api_key
        self.PIXELS_PER_BEAT = 40
        
    def encode_image(self, image_path: str) -> str:
        """Convert image to base64 string for API submission"""
        print(f"Loading image from: {image_path}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        try:
            with open(image_path, "rb") as image_file:
                base64_string = base64.b64encode(image_file.read()).decode('utf-8')
                print(f"Successfully encoded image, length: {len(base64_string)}")
                return base64_string
        except Exception as e:
            raise ValueError(f"Failed to encode image: {str(e)}")

    def analyze_image(self, image_path: str) -> List[Dict]:
        """Use GPT-4o to analyze the piano roll screenshot"""
        print("\nStarting image analysis...")
        base64_image = self.encode_image(image_path)
        
        prompt = """
            You are an expert music notation analyzer. Examine this Ableton Live MIDI piano roll screenshot with precision. For each note block visible:
            1. Determine its exact vertical position (MIDI note number)
            2. Calculate its horizontal position (start beat), pay close attention to the numbers at top that indicate what beat the notes start on.
            3. Measure its length (duration in beats)
            4. If visible, note its velocity (default to 100 if not clear)
            
            Return ONLY this JSON format with no additional text:
            {
                "grid_info": {
                    "pixels_per_beat": int,
                    "pixels_per_semitone": int,
                    "total_beats": int,
                    "lowest_note": int,
                    "highest_note": int
                },
                "notes": [
                    {
                        "midi_note": int,
                        "start_beat": float,
                        "duration_beats": float,
                        "velocity": int
                    }
                ]
            }
        """

        print("Sending request to OpenAI API...")
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4096
            )
            print("Received response from OpenAI API")

            # Extract and validate JSON from response
            response_text = response.choices[0].message.content
            print("\nRaw GPT response:")
            print(response_text)
            print("\n---End of raw response---\n")
            
            # Try to find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
                
            json_str = response_text[json_start:json_end]
            print("Extracted JSON string:")
            print(json_str)
            
            analysis = json.loads(json_str)
            print("\nParsed JSON successfully")
            
            # Validate the response structure
            if 'grid_info' not in analysis or 'notes' not in analysis:
                raise ValueError("Invalid response structure: missing required fields")
                
            # Update internal parameters based on analysis
            self.PIXELS_PER_BEAT = analysis['grid_info']['pixels_per_beat']
            print(f"Found {len(analysis['notes'])} notes in the image")
            return analysis['notes']
            
        except Exception as e:
            print(f"\nERROR during analysis: {str(e)}")
            if 'response' in locals():
                print("\nFull API response:")
                print(response)
            raise ValueError(f"Failed to analyze image: {str(e)}")

    def create_midi(self, notes: List[Dict], output_path: str, bpm: int = 120):
        """Create a MIDI file from the analyzed notes"""
        print(f"\nCreating MIDI file with {len(notes)} notes at {bpm} BPM")
        midi = MIDIFile(1)
        track = 0
        time = 0
        
        try:
            midi.addTrackName(track, time, "Piano Roll")
            midi.addTempo(track, time, bpm)
            
            for i, note in enumerate(notes):
                print(f"Adding note {i+1}: pitch={note['midi_note']}, start={note['start_beat']}, duration={note['duration_beats']}")
                midi.addNote(
                    track=track,
                    channel=0,
                    pitch=note['midi_note'],
                    time=note['start_beat'],
                    duration=note['duration_beats'],
                    volume=note['velocity']
                )
            
            print(f"Writing MIDI file to: {output_path}")    
            with open(output_path, "wb") as midi_file:
                midi.writeFile(midi_file)
            print("Successfully wrote MIDI file")
                
        except Exception as e:
            print(f"ERROR creating MIDI file: {str(e)}")
            raise

    def process_screenshot(self, input_path: str, output_path: str) -> Tuple[bool, str]:
        """Main processing function"""
        print(f"\nProcessing screenshot: {input_path} -> {output_path}")
        try:
            # Validate input file exists
            if not os.path.exists(input_path):
                print(f"ERROR: Input file not found: {input_path}")
                return False, f"Input file not found: {input_path}"
                
            # Validate input file is an image
            try:
                with Image.open(input_path) as img:
                    print(f"Validated image: {img.format} {img.size}")
            except Exception as e:
                print(f"ERROR: Invalid image file: {str(e)}")
                return False, f"Invalid image file: {input_path}"
            
            # Analyze image using GPT-4o
            notes = self.analyze_image(input_path)
            
            # Create MIDI file
            self.create_midi(notes, output_path)
            return True, f"Successfully created MIDI file: {output_path}"
            
        except Exception as e:
            print(f"\nERROR in process_screenshot: {str(e)}")
            return False, f"Error processing screenshot: {str(e)}"


def main():
    import sys
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()
    print("\nStarting Piano Roll Interpreter...")
    
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_image_path> <output_midi_path>")
        return
        
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: Please set OPENAI_API_KEY environment variable")
        return
        
    print("\nArguments:")
    print(f"Input image: {sys.argv[1]}")
    print(f"Output MIDI: {sys.argv[2]}")
    
    interpreter = PianoRollInterpreter(api_key)
    success, message = interpreter.process_screenshot(sys.argv[1], sys.argv[2])
    print(f"\nResult: {'Success' if success else 'Failed'}")
    print(message)


if __name__ == "__main__":
    main()