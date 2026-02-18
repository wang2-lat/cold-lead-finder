import typer
from pathlib import Path
from .scraper import RedditScraper, HNScraper
from .analyzer import LeadAnalyzer
from .exporter import CSVExporter

app = typer.Typer(help="Find cold leads from Reddit and Hacker News")

@app.command()
def search(
    keywords: str = typer.Option(..., "--keywords", "-k", help="Comma-separated keywords to search"),
    platforms: str = typer.Option("reddit,hn", "--platforms", "-p", help="Platforms: reddit,hn"),
    limit: int = typer.Option(50, "--limit", "-l", help="Max posts per platform"),
    output: Path = typer.Option("leads.csv", "--output", "-o", help="Output CSV file"),
    reddit_client_id: str = typer.Option(None, envvar="REDDIT_CLIENT_ID"),
    reddit_client_secret: str = typer.Option(None, envvar="REDDIT_CLIENT_SECRET"),
    openai_api_key: str = typer.Option(None, envvar="OPENAI_API_KEY"),
):
    """Search for potential leads based on keywords."""
    
    keyword_list = [k.strip() for k in keywords.split(",")]
    platform_list = [p.strip() for p in platforms.split(",")]
    
    typer.echo(f"🔍 Searching for: {', '.join(keyword_list)}")
    typer.echo(f"📱 Platforms: {', '.join(platform_list)}")
    
    all_posts = []
    
    # Scrape Reddit
    if "reddit" in platform_list:
        if not reddit_client_id or not reddit_client_secret:
            typer.echo("⚠️  Reddit credentials missing. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET", err=True)
        else:
            typer.echo("📡 Scraping Reddit...")
            reddit = RedditScraper(reddit_client_id, reddit_client_secret)
            all_posts.extend(reddit.search(keyword_list, limit))
    
    # Scrape HN
    if "hn" in platform_list:
        typer.echo("📡 Scraping Hacker News...")
        hn = HNScraper()
        all_posts.extend(hn.search(keyword_list, limit))
    
    typer.echo(f"✅ Found {len(all_posts)} posts")
    
    if not all_posts:
        typer.echo("❌ No posts found. Try different keywords.", err=True)
        raise typer.Exit(1)
    
    # Analyze and generate emails
    if not openai_api_key:
        typer.echo("⚠️  OpenAI API key missing. Set OPENAI_API_KEY for email generation", err=True)
        analyzer = None
    else:
        typer.echo("🤖 Analyzing pain points and generating emails...")
        analyzer = LeadAnalyzer(openai_api_key)
    
    leads = []
    with typer.progressbar(all_posts, label="Processing") as progress:
        for post in progress:
            lead = {
                "platform": post["platform"],
                "author": post["author"],
                "title": post["title"],
                "url": post["url"],
                "content": post["content"][:200],
                "pain_point": "",
                "email_template": ""
            }
            
            if analyzer:
                analysis = analyzer.analyze(post)
                lead["pain_point"] = analysis["pain_point"]
                lead["email_template"] = analysis["email_template"]
            
            leads.append(lead)
    
    # Export to CSV
    exporter = CSVExporter()
    exporter.export(leads, output)
    
    typer.echo(f"✅ Exported {len(leads)} leads to {output}")

if __name__ == "__main__":
    app()