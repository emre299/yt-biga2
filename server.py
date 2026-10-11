import yt_dlp
from mcp.server.fastmcp import FastMCP

# MCP Sunucusunu başlat
mcp = FastMCP("YouTube Music Direct Stream")

@mcp.tool()
async def search_and_play_youtube_music(query: str) -> str:
    """
    YouTube'da bir şarkı arar ve ESP32 cihazının doğrudan çalabileceği 
    ses akış URL'sini (direct audio stream URL) döndürür.
    
    Parametre:
    - query: Aratılacak şarkı adı, sanatçı veya tür (Örn: "Tarkan Şımarık")
    """
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'extract_flat': False, 
    }
    
    search_query = f"ytsearch1:{query}"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            
            if info and 'url' in info:
                title = info.get('title', 'Bilinmeyen Şarkı')
                direct_url = info.get('url')
                return f"BAŞARILI: Şarkı bulundu. Başlık: '{title}'. Çalınacak URL: {direct_url}"
            else:
                return "HATA: Şarkı bulundu ancak URL çıkarılamadı."
                
    except Exception as e:
        return f"HATA: {str(e)}"

if __name__ == "__main__":
    # SSE (Server-Sent Events) üzerinden 8000 portunda dinleyecek
    mcp.run(transport="sse", host="0.0.0.0", port=8000)