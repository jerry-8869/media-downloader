
import os
import sys
import time
import re
import requests
from colorama import init, Fore, Style
from datetime import datetime
import yt_dlp
import platform

# Install required: pip install yt-dlp requests colorama
init(autoreset=True)

class JerryDownloader:
    def __init__(self):
        self.bot_token = None
        self.user_id = None
        self.channel_promo = "📢 Join @jerrybyte for more awesome tools! 📢"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    def display_banner(self):
        """MINIMALIST COOL BANNER - OPTION 4"""
        self.clear_screen()
        
        banner = f"""
{Fore.CYAN}
────────────────────────────────────────────────────────────────
{Fore.MAGENTA}
 JOIN OUR TELEGRAM CHANNELS:- @jerrybyte | @techyspyther | @HeyNarci
{Fore.YELLOW}
                                                       
   ▄▄▄▄▄▄  ▄▄▄▄▄▄▄   ▄▄▄▄▄▄     ▄▄▄▄▄▄     ▄▄▄     
  █▀ ██   █▀██▀▀▀   █▀██▀▀▀█▄  █▀██▀▀▀█▄  █▀██  ██ 
     ██     ██        ██▄▄▄█▀    ██▄▄▄█▀    ██  ██ 
     ██     ████      ██▀▀█▄     ██▀▀█▄     ██  ██ 
     ██     ██      ▄ ██  ██   ▄ ██  ██     ██  ██ 
     ██     ▀█████  ▀██▀  ▀██▀ ▀██▀  ▀██▀   ▀█████▄
 ▄   ██                                     ▄   ██ 
 ▀████▀                                     ▀████▀ 
{Fore.CYAN}
────────────────────────────────────────────────────────────────
{Fore.GREEN}
        ╔══════════════════════════════════════════╗
        ║    ⚡ JERRY SOCIAL MEDIA DOWNLOADER ⚡   ║
        ╚══════════════════════════════════════════╝
{Fore.CYAN}
────────────────────────────────────────────────────────────────
{Fore.MAGENTA}
     YouTube  •   Instagram  •   Facebook  •   Pinterest
{Fore.YELLOW}
            Download Anything and Send to Telegram Bot
{Fore.CYAN}
────────────────────────────────────────────────────────────────
{Style.RESET_ALL}
"""
        print(banner)
    
    def get_credentials(self):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}🔐 TELEGRAM BOT SETUP")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}How to setup:")
        print(f"1. Telegram → Search '@BotFather' → /newbot")
        print(f"2. Copy token (looks like: 1234567890:ABCdefGhIJK...)")
        print(f"3. Search '@userinfobot' → /start → Copy your ID")
        print(f"4. Open your bot → Send /start")
        
        while True:
            print(f"\n{Fore.GREEN}➤ Enter Bot Token: {Fore.YELLOW}", end="")
            self.bot_token = input().strip()
            
            print(f"{Fore.GREEN}➤ Enter Your User ID: {Fore.YELLOW}", end="")
            self.user_id = input().strip()
            
            if self.test_bot_token():
                return True
            else:
                print(f"\n{Fore.RED}❌ Invalid credentials! Try again or press Ctrl+C to exit.")
                retry = input(f"{Fore.YELLOW}Retry? (y/n): {Fore.GREEN}").strip().lower()
                if retry != 'y':
                    return False
    
    def test_bot_token(self):
        """Test if bot token is valid"""
        try:
            test_url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    bot_name = data["result"]["first_name"]
                    print(f"{Fore.GREEN}✅ Connected to @{data['result']['username']} ({bot_name})")
                    return True
            return False
        except:
            return False
    
    def show_menu(self):
        menu = f"""
{Fore.CYAN}{'='*60}
{Fore.YELLOW}📱 SELECT PLATFORM
{Fore.CYAN}{'='*60}
{Fore.GREEN}[1] {Fore.WHITE}YouTube 📺
{Fore.GREEN}[2] {Fore.WHITE}Instagram 📸
{Fore.GREEN}[3] {Fore.WHITE}Facebook 📘
{Fore.GREEN}[4] {Fore.WHITE}Pinterest 📌
{Fore.GREEN}[5] {Fore.WHITE}History 📜
{Fore.GREEN}[6] {Fore.WHITE}Settings ⚙️
{Fore.GREEN}[7] {Fore.WHITE}Exit 🚪
{Fore.CYAN}{'='*60}
{Fore.YELLOW}➤ Select option (1-7): {Fore.GREEN}"""
        
        return input(menu).strip()
    
    def download_youtube(self, url):
        """Download YouTube videos"""
        try:
            print(f"\n{Fore.CYAN}⏬ Downloading YouTube video...")
            
            if not os.path.exists('downloads'):
                os.makedirs('downloads')
            
            ydl_opts = {
                'format': 'best[height<=720]',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Fix extension
                base_name = os.path.splitext(filename)[0]
                for ext in ['.mp4', '.webm', '.mkv']:
                    if os.path.exists(base_name + ext):
                        filename = base_name + ext
                        break
                
                title = info.get('title', 'YouTube Video')[:50]
                return filename, title
                
        except Exception as e:
            print(f"{Fore.RED}❌ YouTube error: {str(e)[:100]}")
            return None, None
    
    def download_instagram(self, url):
        """Download Instagram content"""
        try:
            print(f"\n{Fore.MAGENTA}⏬ Downloading Instagram post...")
            
            
            clean_url = url.split('?')[0]
            
            
            try:
                ydl_opts = {
                    'outtmpl': 'downloads/instagram_%(id)s.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'progress_hooks': [self.progress_hook],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(clean_url, download=True)
                    
                    
                    for file in os.listdir('downloads'):
                        if file.startswith('instagram_'):
                            filename = f"downloads/{file}"
                            title = "Instagram Post"
                            if '/reel/' in clean_url:
                                title = "Instagram Reel"
                            elif '/stories/' in clean_url:
                                title = "Instagram Story"
                            return filename, title
            except:
                pass
            
            
            return self.direct_download(clean_url, "instagram")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Instagram error: {str(e)[:100]}")
            return None, None
    
    def download_facebook(self, url):
        """Download Facebook videos"""
        try:
            print(f"\n{Fore.BLUE}⏬ Downloading Facebook video...")
            
            # Try yt-dlp
            ydl_opts = {
                'outtmpl': 'downloads/facebook_%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                
                base_name = os.path.splitext(filename)[0]
                for ext in ['.mp4', '.webm']:
                    if os.path.exists(base_name + ext):
                        filename = base_name + ext
                        break
                
                return filename, info.get('title', 'Facebook Video')[:50]
                
        except:
            return self.direct_download(url, "facebook")
    
    def download_pinterest(self, url):
        """Download Pinterest content"""
        print(f"\n{Fore.RED}⏬ Downloading Pinterest content...")
        return self.direct_download(url, "pinterest")
    
    def direct_download(self, url, platform_name):
        """Direct download from URL"""
        try:
            response = self.session.get(url, stream=True, timeout=30)
            
            if response.status_code == 200:
                if not os.path.exists('downloads'):
                    os.makedirs('downloads')
                
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Get file type
                content_type = response.headers.get('content-type', '')
                if 'video' in content_type or '.mp4' in url.lower():
                    ext = '.mp4'
                elif 'image' in content_type or any(img in url.lower() for img in ['.jpg', '.jpeg', '.png', '.gif']):
                    ext = '.jpg'
                else:
                    ext = '.mp4'
                
                filename = f"downloads/{platform_name}_{timestamp}{ext}"
                
                # Download with progress
                print(f"{Fore.CYAN}⬇️ Downloading...", end='', flush=True)
                
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            print(f"{Fore.GREEN}▊", end='', flush=True)
                
                print(f"\n{Fore.GREEN}✅ Download complete!")
                return filename, f"{platform_name.capitalize()} Content"
            else:
                print(f"{Fore.RED}❌ Failed: HTTP {response.status_code}")
                return None, None
                
        except Exception as e:
            print(f"{Fore.RED}❌ Download error: {str(e)}")
            return None, None
    
    def progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            if '_percent_str' in d:
                percent = d['_percent_str'].strip()
                print(f"\r{Fore.CYAN}⏬ {percent}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n{Fore.GREEN}✅ Processing...")
    
    def send_to_telegram(self, filepath, title):
        """Send file to Telegram"""
        try:
            if not filepath or not os.path.exists(filepath):
                print(f"{Fore.RED}❌ File not found!")
                return False
            
            print(f"\n{Fore.CYAN}📤 Sending to Telegram...")
            
            # Check file size
            file_size = os.path.getsize(filepath)
            if file_size > 50 * 1024 * 1024:
                print(f"{Fore.RED}❌ File too large! (Max 50MB)")
                return False
            
            # Prepare caption
            caption = f"""
🎬 *{title}*

✅ Downloaded with Jerry Tools
{self.channel_promo}

📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # Read file
            with open(filepath, 'rb') as file:
                file_data = file.read()
            
            filename = os.path.basename(filepath)
            file_lower = filepath.lower()
            
            # Determine endpoint
            if any(ext in file_lower for ext in ['.mp4', '.mov', '.avi', '.mkv']):
                endpoint = f"https://api.telegram.org/bot{self.bot_token}/sendVideo"
                files = {'video': (filename, file_data)}
            elif any(ext in file_lower for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                endpoint = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
                files = {'photo': (filename, file_data)}
            else:
                endpoint = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
                files = {'document': (filename, file_data)}
            
            # Send request
            data = {
                'chat_id': self.user_id,
                'caption': caption,
                'parse_mode': 'Markdown'
            }
            
            response = self.session.post(endpoint, files=files, data=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print(f"{Fore.GREEN}✅ Sent to Telegram!")
                    return True
                else:
                    print(f"{Fore.RED}❌ API error: {result.get('description', 'Unknown')}")
                    return False
            else:
                print(f"{Fore.RED}❌ Failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Send error: {str(e)}")
            return False
    
    def save_history(self, platform, url, filename):
        """Save download history"""
        try:
            with open("download_history.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} | {platform} | {url[:50]}... | {filename}\n")
        except:
            pass
    
    def show_history(self):
        """Show download history"""
        if os.path.exists("download_history.txt"):
            self.display_banner()
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.YELLOW}📜 DOWNLOAD HISTORY")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            with open("download_history.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    for line in lines[-10:]:
                        print(f"{Fore.GREEN}→ {Fore.WHITE}{line.strip()}")
                else:
                    print(f"{Fore.YELLOW}No history yet!")
        else:
            print(f"\n{Fore.YELLOW}No download history yet!")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def show_settings(self):
        """Show settings menu"""
        self.display_banner()
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}⚙️ SETTINGS")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}Current:")
        print(f"{Fore.CYAN}• Bot: {Fore.YELLOW}{'*' * 20 if self.bot_token else 'Not set'}")
        print(f"{Fore.CYAN}• User ID: {Fore.YELLOW}{self.user_id if self.user_id else 'Not set'}")
        
        print(f"\n{Fore.GREEN}Options:")
        print(f"{Fore.CYAN}[1] {Fore.WHITE}Change Credentials")
        print(f"{Fore.CYAN}[2] {Fore.WHITE}Clear History")
        print(f"{Fore.CYAN}[3] {Fore.WHITE}Back")
        
        choice = input(f"\n{Fore.YELLOW}➤ Select: {Fore.GREEN}").strip()
        
        if choice == '1':
            self.get_credentials()
        elif choice == '2':
            if os.path.exists("download_history.txt"):
                os.remove("download_history.txt")
                print(f"{Fore.GREEN}✅ History cleared!")
                time.sleep(1)
    
    def download_content(self, choice, url):
        """Handle downloading based on platform choice"""
        platforms = {
            '1': ('YouTube', self.download_youtube),
            '2': ('Instagram', self.download_instagram),
            '3': ('Facebook', self.download_facebook),
            '4': ('Pinterest', self.download_pinterest)
        }
        
        if choice in platforms:
            platform_name, download_func = platforms[choice]
            print(f"\n{Fore.YELLOW}🔄 Processing {platform_name} link...")
            return download_func(url)
        
        return None, None
    
    def run(self):
        """Main program loop"""
        # Setup
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        
        # Show banner
        self.display_banner()
        
        # Get credentials
        print(f"\n{Fore.YELLOW}🔧 Initial setup required...")
        if not self.get_credentials():
            print(f"\n{Fore.RED}❌ Setup incomplete. Exiting.")
            return
        
        # Main loop
        while True:
            self.display_banner()
            choice = self.show_menu()
            
            if choice == '7':
                print(f"\n{Fore.YELLOW}👋 Thanks for using Jerry Downloader!")
                print(f"{Fore.CYAN}{self.channel_promo}")
                break
            
            elif choice == '5':
                self.show_history()
                continue
            
            elif choice == '6':
                self.show_settings()
                continue
            
            elif choice in ['1', '2', '3', '4']:
                # Get URL
                platforms_name = {
                    '1': 'YouTube', '2': 'Instagram', 
                    '3': 'Facebook', '4': 'Pinterest'
                }
                
                print(f"\n{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}📥 {platforms_name[choice]} URL")
                print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
                print(f"\n{Fore.GREEN}➤ Paste URL: {Fore.YELLOW}", end="")
                url = input().strip()
                
                if not url or 'http' not in url:
                    print(f"{Fore.RED}❌ Invalid URL!")
                    time.sleep(1)
                    continue
                
                # Download
                filepath, title = self.download_content(choice, url)
                
                if filepath and os.path.exists(filepath):
                    print(f"{Fore.GREEN}✅ Download successful!")
                    
                    # Send to Telegram
                    if self.send_to_telegram(filepath, title or platforms_name[choice]):
                        self.save_history(platforms_name[choice], url, os.path.basename(filepath))
                        
                        # Success message
                        print(f"\n{Fore.CYAN}{'='*60}")
                        print(f"{Fore.GREEN}🎉 SUCCESS!")
                        print(f"{Fore.CYAN}{'='*60}")
                        print(f"{Fore.YELLOW}📱 Check your Telegram!")
                        print(f"{Fore.MAGENTA}{self.channel_promo}")
                        print(f"{Fore.CYAN}{'='*60}")
                    
                    # Cleanup
                    print(f"\n{Fore.YELLOW}🗑️ Delete file? (y/n): {Fore.GREEN}", end="")
                    if input().strip().lower() == 'y':
                        try:
                            os.remove(filepath)
                            print(f"{Fore.GREEN}✅ Cleaned up!")
                        except:
                            pass
                else:
                    print(f"{Fore.RED}❌ Download failed!")
                    print(f"{Fore.YELLOW}💡 Tips: Check if content is public/accessible")
                
                input(f"\n{Fore.CYAN}Press Enter to continue...")
            
            else:
                print(f"{Fore.RED}❌ Invalid choice!")
                time.sleep(1)

def main():
    """Main function"""
    print(f"{Fore.YELLOW}🚀 Starting Jerry Downloader...")
    time.sleep(1)
    
    
    try:
        import yt_dlp
        import requests
    except ImportError:
        print(f"{Fore.RED}❌ Missing dependencies!")
        print(f"{Fore.YELLOW}Run: pip install yt-dlp requests colorama")
        input("Press Enter to exit...")
        return
    
    
    try:
        downloader = JerryDownloader()
        downloader.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n{Fore.RED}💥 Error: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
