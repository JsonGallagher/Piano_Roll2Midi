# Piano Roll Interpreter

Convert DAW piano roll screenshots into MIDI files using AI-powered image recognition. This tool analyzes screenshots of piano roll patterns from digital audio workstations and automatically generates corresponding MIDI files, making it easy to transfer musical ideas between different DAWs or share patterns with other musicians.

## Features

- Automated recognition of piano roll notes from screenshots
- Accurate detection of note positions, lengths, and velocities
- MIDI file generation with preserved timing and velocity information
- Support for complex musical patterns
- Detailed logging for troubleshooting

## Prerequisites

- Python 3.8+
- OpenAI API key (GPT-4V access required)
- Required Python packages:
  ```
  openai
  python-dotenv
  Pillow
  midiutil
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/piano-roll-interpreter.git
   cd piano-roll-interpreter
   ```

2. Set up a virtual environment:

   **macOS/Linux:**
   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate virtual environment
   source venv/bin/activate   # For bash/zsh
   source venv/bin/activate.fish   # For fish
   ```

   **Windows:**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. When you're done working on the project, deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Usage

Make sure your virtual environment is activated, then run the script from the command line with two arguments:
1. Path to the input screenshot
2. Desired output MIDI file path

```bash
python piano_roll_interpreter.py input_screenshot.png output_pattern.mid
```

### Example:
```bash
python piano_roll_interpreter.py "./screenshots/pattern1.png" "./midi/pattern1.mid"
```

## How It Works

1. **Image Processing**: The tool takes a screenshot of your DAW's piano roll as input.
2. **AI Analysis**: Using GPT-4V, it analyzes the image to detect:
   - Note positions (MIDI note numbers)
   - Start times (in beats)
   - Note durations
   - Velocity values
3. **MIDI Generation**: The detected notes are converted into a MIDI file that preserves all musical information.

## Best Practices for Screenshots

For optimal results:
- Ensure the piano roll grid is clearly visible
- Include the beat markers at the top of the piano roll
- Make sure note blocks are distinct and not overlapping
- Capture the entire pattern you want to convert
- Use a clean view without unnecessary UI elements

## Error Handling

The script includes comprehensive error handling and logging:
- Validates input files exist and are valid images
- Checks API key availability
- Verifies JSON response structure
- Provides detailed error messages for troubleshooting

## Project Structure

```
piano-roll-interpreter/
├── piano_roll_interpreter.py   # Main script
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
└── README.md                 # Documentation
```

## Troubleshooting

Common issues:
- If you get a "command not found" error, make sure your virtual environment is activated
- If you see import errors, verify that all dependencies were installed while the virtual environment was activated
- For permission issues on macOS/Linux when creating the virtual environment, try using `sudo python3 -m venv venv`

## Limitations

- Currently optimized for Ableton Live piano roll screenshots
- Requires clear, high-quality screenshots
- API key with GPT-4V access is required
- Processing time depends on image complexity and API response time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses OpenAI's GPT-4V for image analysis
- Built with Python's `midiutil` library for MIDI file creation
