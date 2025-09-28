<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ignitos Telegram Bot Deployment Guide</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0d1117; /* GitHub Dark Background */
            color: #c9d1d9; /* GitHub Text Color */
        }
        .code-container {
            position: relative;
            background-color: #161b22; /* Slightly darker code block background */
            border-radius: 6px;
            padding: 1.5rem 1rem 1rem 1rem;
            margin-bottom: 1.5rem;
            overflow-x: auto;
            white-space: nowrap;
        }
        .copy-btn {
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            border-radius: 4px;
            background-color: #238636; /* GitHub green */
            color: white;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .copy-btn:hover {
            background-color: #2ea043;
        }
        .terminal-prompt {
            color: #8b949e; /* Faded gray for comments/prompts */
            user-select: none; /* Make the prompt unselectable */
            display: block;
            margin-bottom: 0.25rem;
        }
        .terminal-command {
            color: #58a6ff; /* Blue for the command text */
            font-family: monospace;
            font-size: 0.95rem;
            display: inline-block;
            white-space: pre;
        }
        .table-header {
            background-color: #1f6feb; /* Blue header for tables */
            color: white;
        }
    </style>
</head>
<body class="p-4 md:p-8">

    <div class="max-w-4xl mx-auto">
        
        <!-- Header Section -->
        <header class="text-center mb-10">
            <h1 class="text-4xl md:text-5xl font-extrabold text-[#58a6ff] mb-2">
                <span class="inline-block transform rotate-[-5deg] mr-2">🚀</span> IGNITOS TELEGRAM BOT
            </h1>
            <p class="text-lg md:text-xl font-semibold text-gray-400">
                Telegram Automation on the Gemini Platform
            </p>
            <p class="text-md text-gray-500 mt-2">
                A self-bot framework packed with auto-reply features and modular AI plugins.
            </p>
        </header>

        <!-- Placeholder Image/Banner -->
        <div class="mb-8 rounded-lg overflow-hidden border border-gray-700">
            <img src="https://placehold.co/1000x250/161b22/8b949e?text=Modular+Telegram+Self-Bot+with+AI+%26+Image+Generation" alt="Modular Telegram Bot with AI and Image Generation" class="w-full h-auto">
        </div>

        <!-- Features Table -->
        <section class="mb-10">
            <h2 class="text-2xl font-bold mb-4 border-b border-gray-700 pb-2">✨ Features at a Glance</h2>
            <div class="overflow-x-auto rounded-lg">
                <table class="min-w-full text-sm">
                    <thead>
                        <tr class="bg-blue-600 text-white">
                            <th class="py-2 px-4 text-left rounded-tl-lg">Command Type</th>
                            <th class="py-2 px-4 text-left">Prefix</th>
                            <th class="py-2 px-4 text-left">Description</th>
                            <th class="py-2 px-4 text-left rounded-tr-lg">Powered By</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-700 bg-gray-800">
                        <tr>
                            <td class="py-2 px-4 font-semibold">AI Generation</td>
                            <td class="py-2 px-4">`.ai` / `/ai`</td>
                            <td class="py-2 px-4">Answers questions using the Gemini API with Google Search grounding.</td>
                            <td class="py-2 px-4">`plugins/ai.py`</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">Image Generation</td>
                            <td class="py-2 px-4">`.img` / `/img`</td>
                            <td class="py-2 px-4">Generates an image using the Imagen 3 API (Text-to-Image).</td>
                            <td class="py-2 px-4">`plugins/image_gen.py`</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">Auto-Reply</td>
                            <td class="py-2 px-4">Core</td>
                            <td class="py-2 px-4">Automatically replies to private messages when set to `/away`.</td>
                            <td class="py-2 px-4">`main.py`</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Prerequisites -->
        <section class="mb-10 p-4 bg-[#161b22] rounded-lg border border-gray-700">
            <h2 class="text-2xl font-bold mb-4 border-b border-gray-700 pb-2 text-yellow-300">⚙️ Prerequisites</h2>
            <ul class="list-disc list-inside space-y-2 text-gray-400">
                <li>**A Linux VPS:** Running Ubuntu, Debian, or CentOS.</li>
                <li>**SSH Access:** To connect to your server.</li>
                <li>**Bot Code:** The full project directory, including `main.py` and `requirements.txt`.</li>
                <li class="mt-4">**Credentials Needed:**
                    <ul class="list-disc list-inside ml-5">
                        <li>Telegram API ID and API Hash (from [my.telegram.org](https://my.telegram.org)).</li>
                        <li>BotFather Bot Token (for the remote control bot).</li>
                        <li>**Gemini API Key** (for `.ai` and `.img` commands).</li>
                    </ul>
                </li>
            </ul>
        </section>
        
        <!-- Deployment Steps -->
        <section class="mb-10">
            <h2 class="text-3xl font-bold mb-6 text-[#238636]">🛠️ Deployment Steps (Linux VPS)</h2>

            <!-- Step 1 -->
            <h3 class="text-xl font-semibold mb-2 text-blue-400">Step 1: Prepare the VPS Environment</h3>
            <p class="mb-2 text-gray-400">Log in to your VPS via SSH to set up the necessary environment.</p>
            <div class="code-container" data-command="sudo apt update && sudo apt install python3 python3-pip git -y">
                <span class="copy-btn">Copy</span>
                <span class="terminal-prompt"># Update package list and install Python 3, pip, and git</span>
                <code class="terminal-command">$ sudo apt update && sudo apt install python3 python3-pip git -y</code>
            </div>

            <!-- Step 2 -->
            <h3 class="text-xl font-semibold mb-2 text-blue-400">Step 2: Set Up Project Structure and Virtual Environment</h3>
            <div class="code-container" data-command="sudo apt install python3-venv -y
mkdir ignitos_bot && cd ignitos_bot
python3 -m venv venv
source venv/bin/activate">
                <span class="copy-btn">Copy</span>
                <span class="terminal-prompt"># Install venv, create directory, and activate venv</span>
                <code class="terminal-command">$ sudo apt install python3-venv -y</code>
                <code class="terminal-command block">$ mkdir ignitos_bot && cd ignitos_bot</code>
                <code class="terminal-command block">$ python3 -m venv venv</code>
                <code class="terminal-command block">$ source venv/bin/activate</code>
            </div>

            <!-- Step 3 -->
            <h3 class="text-xl font-semibold mb-2 text-blue-400">Step 3: Clone Code and Install Dependencies</h3>
            <div class="code-container" data-command="git clone [YOUR_REPOSITORY_URL] .
pip install -r requirements.txt">
                <span class="copy-btn">Copy</span>
                <span class="terminal-prompt"># Clone your repository (REPLACE with your actual GitHub URL)</span>
                <code class="terminal-command block">$ git clone [YOUR_REPOSITORY_URL] .</code>
                <span class="terminal-prompt block mt-2"># Install all required Python libraries. Ensure (venv) is active.</span>
                <code class="terminal-command block">$ pip install -r requirements.txt</code>
            </div>
            
            <!-- Step 4 -->
            <h3 class="text-xl font-semibold mb-2 text-blue-400">Step 4: Run for Initial Configuration</h3>
            <p class="mb-2 text-gray-400">The script will guide you through entering all your API keys and logging into your Telegram account to create the secure session file.</p>
            <div class="code-container" data-command="python3 main.py">
                <span class="copy-btn">Copy</span>
                <span class="terminal-prompt"># Run the script and follow the on-screen prompts</span>
                <code class="terminal-command">$ python3 main.py</code>
            </div>

            <!-- Step 5 -->
            <h3 class="text-xl font-semibold mb-2 text-blue-400">Step 5: Run the Bot Continuously (24/7)</h3>
            <p class="mb-2 text-gray-400">Use `screen` to keep the bot running after you disconnect from SSH.</p>
            <div class="code-container" data-command="sudo apt install screen -y
screen -S ignitos_session
python3 main.py">
                <span class="copy-btn">Copy</span>
                <span class="terminal-prompt"># Install screen (if needed)</span>
                <code class="terminal-command block">$ sudo apt install screen -y</code>
                <span class="terminal-prompt block mt-2"># Start a new session and launch the bot</span>
                <code class="terminal-command block">$ screen -S ignitos_session</code>
                <code class="terminal-command block">$ python3 main.py</code>
            </div>
            <p class="text-sm text-gray-500 mt-2">**To Detach:** Press **Ctrl + A** then **D**. The bot will keep running!</p>
        </section>

        <!-- Command Reference -->
        <section class="mb-10">
            <h2 class="text-3xl font-bold mb-4 border-b border-gray-700 pb-2 text-green-400">📚 Bot Command Reference</h2>
            <div class="overflow-x-auto rounded-lg">
                <table class="min-w-full text-sm">
                    <thead>
                        <tr class="bg-gray-700 text-white">
                            <th class="py-2 px-4 text-left rounded-tl-lg">Function</th>
                            <th class="py-2 px-4 text-left">User Bot Command (Self)</th>
                            <th class="py-2 px-4 text-left">Control Bot Command</th>
                            <th class="py-2 px-4 text-left rounded-tr-lg">Example Usage</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-700 bg-gray-800">
                        <tr>
                            <td class="py-2 px-4 font-semibold">AI Question</td>
                            <td class="py-2 px-4">`.ai [prompt]`</td>
                            <td class="py-2 px-4">`/ai [prompt]`</td>
                            <td class="py-2 px-4 font-mono text-xs">`.ai What is the capital of Canada?`</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">Image Generation</td>
                            <td class="py-2 px-4">`.img [prompt]`</td>
                            <td class="py-2 px-4">`/img [prompt]`</td>
                            <td class="py-2 px-4 font-mono text-xs">`.img A hyperrealistic neon tiger.`</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">Check Latency</td>
                            <td class="py-2 px-4">`.ping`</td>
                            <td class="py-2 px-4">-</td>
                            <td class="py-2 px-4 font-mono text-xs">`.ping`</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">Enable Auto-Reply</td>
                            <td class="py-2 px-4">`.away`</td>
                            <td class="py-2 px-4">-</td>
                            <td class="py-2 px-4 font-mono text-xs">`.away`</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">Disable Auto-Reply</td>
                            <td class="py-2 px-4">`.online`</td>
                            <td class="py-2 px-4">-</td>
                            <td class="py-2 px-4 font-mono text-xs">`.online`</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">Set Offline Message</td>
                            <td class="py-2 px-4">`.editoff [new message]`</td>
                            <td class="py-2 px-4">-</td>
                            <td class="py-2 px-4 font-mono text-xs">`.editoff I am busy coding.`</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Management Commands -->
        <section class="mb-10">
            <h3 class="text-xl font-bold mb-4 border-b border-gray-700 pb-2 text-yellow-500">💻 Console Management Commands</h3>
            <div class="overflow-x-auto rounded-lg">
                <table class="min-w-full text-sm">
                    <thead>
                        <tr class="bg-gray-700 text-white">
                            <th class="py-2 px-4 text-left rounded-tl-lg">Action</th>
                            <th class="py-2 px-4 text-left">Command</th>
                            <th class="py-2 px-4 text-left rounded-tr-lg">Notes</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-700 bg-gray-800">
                        <tr>
                            <td class="py-2 px-4 font-semibold">Re-attach to console</td>
                            <td class="py-2 px-4 font-mono">`screen -r ignitos_session`</td>
                            <td class="py-2 px-4">See the bot's live logs and output.</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">Stop the bot entirely</td>
                            <td class="py-2 px-4 font-mono">Re-attach, then `Ctrl + C`</td>
                            <td class="py-2 px-4">Stops the Python script inside the screen.</td>
                        </tr>
                        <tr>
                            <td class="py-2 px-4 font-semibold">List all active sessions</td>
                            <td class="py-2 px-4 font-mono">`screen -ls`</td>
                            <td class="py-2 px-4">Shows all detached sessions.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <footer class="text-center mt-10 text-sm text-gray-500">
            Made with ❤️ for the Telegram Community | This document is an interactive deployment guide.
        </footer>

    </div>

    <script>
        // JavaScript for Copy-to-Clipboard functionality
        document.addEventListener('DOMContentLoaded', () => {
            const codeContainers = document.querySelectorAll('.code-container');

            codeContainers.forEach(container => {
                const copyBtn = container.querySelector('.copy-btn');
                const commandBlock = container.getAttribute('data-command');

                copyBtn.addEventListener('click', () => {
                    if (!commandBlock) return;

                    // Use execCommand('copy') for better iframe compatibility
                    const textarea = document.createElement('textarea');
                    textarea.value = commandBlock.replace(/\$/g, '').trim(); // Remove the terminal prompt character
                    textarea.style.position = 'fixed'; // Prevent scrolling to bottom
                    document.body.appendChild(textarea);
                    textarea.focus();ac
                    textarea.select();

                    try {
                        const successful = document.execCommand('copy');
                        if (successful) {
                            copyBtn.textContent = 'Copied!';
                            setTimeout(() => {
                                copyBtn.textContent = 'Copy';
                            }, 2000);
                        } else {
                            // Fallback for failed copy (less common now)
                            copyBtn.textContent = 'Failed';
                            setTimeout(() => {
                                copyBtn.textContent = 'Copy';
                            }, 2000);
                        }
                    } catch (err) {
                        console.error('Copy command failed:', err);
                        copyBtn.textContent = 'Error';
                        setTimeout(() => {
                            copyBtn.textContent = 'Copy';
                        }, 2000);
                    }

                    document.body.removeChild(textarea);
                });
            });
        });
    </script>
</body>
</html>
