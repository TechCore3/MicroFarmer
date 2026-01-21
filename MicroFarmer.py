import asyncio
import random
import time
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from playwright.async_api import async_playwright

# --- COMPONENTS FOR PROCEDURAL GENERATION ---
TOPICS = [
    "quantum physics", "space exploration", "renewable energy", "artificial intelligence",
    "paleontology", "deep sea creatures", "ancient rome", "renaissance art",
    "healthy recipes", "yoga", "world travel", "sci-fi movies",
    "python programming", "electric cars", "sustainability", "gardening",
    "minimalist living", "jazz history", "classic literature", "modern architecture",
    "baking", "digital photography", "stargazing", "wildlife conservation",
    "neuroscience", "geopolitics", "financial planning", "investing",
    "meditation", "learning languages", "astronomy", "coding",
    "home decor", "fashion", "cooking", "biology", "creative writing"
]

MODIFIERS = [
    "latest news on", "best techniques for", "history of", "how to start",
    "future of", "top 10", "beginners guide to", "advanced concepts in",
    "current trends in", "benefits of", "importance of", "evolution of",
    "unusual facts about", "scientific breakthroughs in", "tutorial on"
]

CONTEXTS = [
    "in 2026", "for professionals", "at home", "on a budget",
    "for students", "worldwide", "in modern society", "explained simple",
    "step by step", "with examples", "illustrated", "documentary"
]

def generate_procedural_query():
    topic = random.choice(TOPICS)
    modifier = random.choice(MODIFIERS)
    context = random.choice(CONTEXTS)
    structure = random.randint(1, 3)
    if structure == 1: return f"{modifier} {topic}"
    elif structure == 2: return f"{topic} {context}"
    else: return f"{modifier} {topic} {context}"

class RewardsFarmerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Edge Rewards Farmer")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        
        self.running = False
        self.loop = None
        
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Execution Settings", style="Header.TLabel").pack(pady=(0, 15))

        # Max Searches
        ttk.Label(main_frame, text="Number of Searches:").pack(anchor=tk.W)
        self.max_searches_var = tk.IntVar(value=30)
        ttk.Entry(main_frame, textvariable=self.max_searches_var).pack(fill=tk.X, pady=(0, 10))

        # Delay Min
        ttk.Label(main_frame, text="Min Delay (seconds):").pack(anchor=tk.W)
        self.min_delay_var = tk.DoubleVar(value=5.0)
        ttk.Entry(main_frame, textvariable=self.min_delay_var).pack(fill=tk.X, pady=(0, 10))

        # Delay Max
        ttk.Label(main_frame, text="Max Delay (seconds):").pack(anchor=tk.W)
        self.max_delay_var = tk.DoubleVar(value=10.0)
        ttk.Entry(main_frame, textvariable=self.max_delay_var).pack(fill=tk.X, pady=(0, 20))

        # Status Label
        self.status_var = tk.StringVar(value="Status: Ready")
        ttk.Label(main_frame, textvariable=self.status_var, foreground="blue").pack(pady=(0, 10))

        # Progress
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 20))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        self.start_btn = ttk.Button(button_frame, text="Start Farming", command=self.start_task)
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_task, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        ttk.Label(main_frame, text="Close Edge before starting!", font=("Segoe UI", 8, "italic"), foreground="gray").pack(pady=(15, 0))

    def log(self, message):
        self.status_var.set(f"Status: {message}")
        print(message)

    def close_edge_processes(self):
        self.log("Closing existing Edge instances...")
        try:
            # /F is force, /IM is image name, /T is tree (children)
            # We use a silent call to avoid popping a console window
            os.system('taskkill /F /IM msedge.exe /T >nul 2>&1')
            time.sleep(1) # Small buffer for OS to release files
        except Exception as e:
            self.log(f"Warning: Could not close Edge: {e}")

    def start_task(self):
        if not self.running:
            self.close_edge_processes()
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            threading.Thread(target=self.run_async_loop, daemon=True).start()

    def stop_task(self):
        if self.running:
            self.running = False
            self.log("Stopping...")

    def run_async_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.automation_main())
        self.running = False
        self.root.after(0, self.reset_ui)

    def reset_ui(self):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.log("Ready")

    async def perform_search(self, page, query):
        self.log(f"Searching: {query}")
        try:
            if "bing.com" not in page.url:
                await page.goto("https://www.bing.com")
                await asyncio.sleep(2)
            
            search_bar = page.locator("#sb_form_q")
            await search_bar.click()
            await search_bar.fill("") 
            await search_bar.type(query, delay=random.randint(50, 150))
            await search_bar.press("Enter")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(random.uniform(3, 5))
            
            scroll_amount = random.randint(200, 600)
            await page.evaluate(f"window.scrollTo(0, {scroll_amount})")
        except Exception as e:
            self.log(f"Search Error: {e}")

    async def automation_main(self):
        max_searches = self.max_searches_var.get()
        delay_min = self.min_delay_var.get()
        delay_max = self.max_delay_var.get()
        user_data_dir = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Edge", "User Data")

        async with async_playwright() as p:
            try:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    channel="msedge",
                    headless=False,
                    args=["--profile-directory=Default"],
                    slow_mo=500
                )
            except Exception as e:
                self.log(f"Launch Fail: {e}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Could not launch Edge. Make sure it's closed!\n\n{e}"))
                return

            page = context.pages[0] if context.pages else await context.new_page()
            searches_performed = 0
            used_queries = set()

            while searches_performed < max_searches and self.running:
                query = generate_procedural_query()
                if query in used_queries: continue
                used_queries.add(query)
                
                searches_performed += 1
                self.progress_var.set((searches_performed / max_searches) * 100)
                
                await self.perform_search(page, query)
                
                if searches_performed < max_searches and self.running:
                    wait_time = random.uniform(delay_min, delay_max)
                    self.log(f"Waiting {wait_time:.1f}s...")
                    await asyncio.sleep(wait_time)

            self.log("Finished!")
            await asyncio.sleep(2)
            await context.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RewardsFarmerGUI(root)
    root.mainloop()
