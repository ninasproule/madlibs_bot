# Discord MadLibs Bot

A discord bot for playing, and creating your own madlibs that others can play!

## Features

- **Play MadLibs**: Choose from available templates or get a random one
- **Create Custom Templates**: Make your own MadLib stories for others to enjoy
- **Template Management**: Browse all available MadLibs with paged lists
- **Interactive Gameplay**: Bot guides players through each word prompt
- **Persistent Storage**: All custom templates are saved and persist between bot restarts
- **User-Friendly Interface**: Rich Discord embeds for better user experience

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `$play [title]` | Play a MadLib (random if no title specified) | `$play` or `$play wedding vows` |
| `$new` | Create a new MadLib template | `$new` |
| `$list` | View all available MadLib titles | `$list` |
| `$cancel` | Cancel any running MadLib operations | `$cancel` |
| `$help` | Display help message with all commands | `$help` |

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- A Discord Bot Token

### Step 1: Clone the Repository
```bash
git clone https://github.com/ninasproule/madlibs_bot.git
cd madlibs_bot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
1. Create a `.env` file in the project root:

2. Add your Discord bot token to the `.env` file:
```
DISCORD_TOKEN=your_bot_token_here
```

### Step 4: Get a Discord Bot Token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Create a bot and copy the token
5. Paste the token in your `.env` file

### Step 5: Invite Bot to Your Server
1. In the Discord Developer Portal, go to "OAuth2" > "URL Generator"
2. Select scopes: `bot`
3. Select bot permissions:
   - Send Messages
   - Add Reactions
   - Read Message History
   - Embed Links
4. Use the generated URL to invite the bot to your server

### Step 6: Run the Bot
```bash
python bot.py
```

## How to Play

### Playing a MadLib
1. Use `$play` for a random MadLib or `$play [title]` for a specific one
2. The bot will prompt you for different types of words (nouns, verbs, adjectives, etc.)
3. Type your word when prompted
4. Enjoy the hilarious results!

### Creating Your Own MadLib
1. Use `$new` to start creating a template
2. Choose option 1️⃣ to create or 2️⃣ to view instructions
3. Write your story, using `<word type>` for blanks (e.g., `<noun>`, `<adjective>`, `<body part>`)
4. Example: `"The <adjective> cat <verb (past-tense)> over the <noun>"`
5. Confirm your template and give it a title

## File Structure

```
madlibs_bot/
├── bot.py                 # Main bot application
├── default_templates.py   # Pre-made MadLib templates
├── storage.py             # JSON storage management
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── .env                   # Environment variables (you create this)
├── madlibs.json           # Stored templates (auto-generated)
└── README.md              # This file
```

## Technical Details

- **Framework**: discord.py
- **Python Version**: 3.8+
- **Command Prefix**: `$`
- **Timeout**: 60 seconds for user responses

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues
- **Bot doesn't respond**: Check if the bot has the necessary permissions in your server
- **Token errors**: Verify your `DISCORD_TOKEN` in the `.env` file
- **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

### Need Help?
- Check the console output for error messages
- Ensure the bot has proper permissions in your Discord server
- Verify all files are in the correct directory structure

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, feel free to:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the command documentation

---

Made with ❤️ for Discordians who love word games!