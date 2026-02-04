#!/usr/bin/env python3
"""
Cold Email Generator - Generate personalized cold emails that get responses
By Bandit 🦝 | raccoons.work

Generates personalized cold emails using prospect research.
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install: pip install requests beautifulsoup4")
    sys.exit(1)

# Try AI providers
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class Prospect:
    """Prospect information for email personalization."""
    name: str
    company: str
    role: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    # Research findings
    company_description: Optional[str] = None
    recent_news: Optional[str] = None
    tech_stack: Optional[str] = None
    pain_points: Optional[str] = None


@dataclass
class EmailConfig:
    """Email generation configuration."""
    sender_name: str
    sender_company: str
    value_prop: str
    cta: str = "quick call"
    tone: str = "professional-friendly"  # professional, casual, professional-friendly
    length: str = "short"  # short, medium


class ProspectResearcher:
    """Research prospects from public information."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (compatible; EmailResearch/1.0)'
    
    def research_website(self, url: str) -> dict:
        """Extract info from company website."""
        try:
            resp = self.session.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Get description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'] if meta_desc else None
            
            # Get title
            title = soup.title.text if soup.title else None
            
            # Look for about text
            about = None
            for selector in ['#about', '.about', '[class*="about"]', 'section']:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text()[:500]
                    if len(text) > 100:
                        about = text
                        break
            
            # Look for tech indicators
            tech_hints = []
            scripts = soup.find_all('script', src=True)
            for s in scripts:
                src = s['src'].lower()
                if 'react' in src: tech_hints.append('React')
                if 'vue' in src: tech_hints.append('Vue')
                if 'angular' in src: tech_hints.append('Angular')
                if 'stripe' in src: tech_hints.append('Stripe')
                if 'intercom' in src: tech_hints.append('Intercom')
                if 'hubspot' in src: tech_hints.append('HubSpot')
            
            return {
                'description': description,
                'title': title,
                'about': about,
                'tech_hints': list(set(tech_hints))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def research(self, prospect: Prospect) -> Prospect:
        """Enrich prospect with research."""
        if prospect.website:
            data = self.research_website(prospect.website)
            if data.get('description'):
                prospect.company_description = data['description']
            if data.get('tech_hints'):
                prospect.tech_stack = ', '.join(data['tech_hints'])
        
        return prospect


class ColdEmailGenerator:
    """Generate personalized cold emails."""
    
    TEMPLATE_PROMPT = """Generate a cold email with these requirements:

PROSPECT:
- Name: {name}
- Company: {company}
- Role: {role}
- Company Description: {company_description}
- Tech Stack: {tech_stack}

SENDER:
- Name: {sender_name}
- Company: {sender_company}
- Value Proposition: {value_prop}
- Desired CTA: {cta}

STYLE:
- Tone: {tone}
- Length: {length} (short=3-4 sentences, medium=5-6 sentences)

RULES:
1. Personalize based on prospect's company/role
2. Lead with value, not features
3. One clear call-to-action
4. No generic flattery ("I love your company!")
5. Sound human, not templated
6. Subject line should create curiosity

Return JSON:
{{
    "subject": "Email subject line",
    "body": "Full email body",
    "follow_up": "Follow-up email if no response (shorter)"
}}"""

    def __init__(self, provider: str = 'auto'):
        self.provider = self._select_provider(provider)
    
    def _select_provider(self, preferred: str) -> str:
        if preferred == 'openai' or (preferred == 'auto' and HAS_OPENAI and os.getenv('OPENAI_API_KEY')):
            return 'openai'
        if preferred == 'anthropic' or (preferred == 'auto' and HAS_ANTHROPIC and os.getenv('ANTHROPIC_API_KEY')):
            return 'anthropic'
        raise RuntimeError("No AI provider. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    
    def generate(self, prospect: Prospect, config: EmailConfig) -> dict:
        """Generate a personalized cold email."""
        prompt = self.TEMPLATE_PROMPT.format(
            name=prospect.name,
            company=prospect.company,
            role=prospect.role or 'Unknown',
            company_description=prospect.company_description or 'Unknown',
            tech_stack=prospect.tech_stack or 'Unknown',
            sender_name=config.sender_name,
            sender_company=config.sender_company,
            value_prop=config.value_prop,
            cta=config.cta,
            tone=config.tone,
            length=config.length
        )
        
        if self.provider == 'openai':
            return self._generate_openai(prompt)
        else:
            return self._generate_anthropic(prompt)
    
    def _generate_openai(self, prompt: str) -> dict:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    def _generate_anthropic(self, prompt: str) -> dict:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model='claude-3-haiku-20240307',
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt + "\n\nRespond with JSON only."}]
        )
        content = response.content[0].text
        if '```' in content:
            content = content.split('```')[1].replace('json', '').strip()
        return json.loads(content)


def format_email(email: dict, prospect: Prospect) -> str:
    """Format email for display."""
    output = []
    output.append("=" * 60)
    output.append(f"TO: {prospect.name} <{prospect.email or 'email@example.com'}>")
    output.append(f"SUBJECT: {email['subject']}")
    output.append("=" * 60)
    output.append("")
    output.append(email['body'])
    output.append("")
    output.append("-" * 60)
    output.append("FOLLOW-UP (if no response after 3-5 days):")
    output.append("-" * 60)
    output.append(email.get('follow_up', 'N/A'))
    output.append("")
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Cold Email Generator - Personalized emails that get responses',
        epilog='By Bandit 🦝 | raccoons.work'
    )
    
    # Prospect args
    parser.add_argument('--name', required=True, help='Prospect name')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--role', help='Prospect role/title')
    parser.add_argument('--email', help='Prospect email')
    parser.add_argument('--website', help='Company website (for research)')
    
    # Sender args
    parser.add_argument('--sender', required=True, help='Your name')
    parser.add_argument('--sender-company', required=True, help='Your company')
    parser.add_argument('--value-prop', required=True, help='Your value proposition')
    parser.add_argument('--cta', default='quick call', help='Call to action')
    
    # Style args
    parser.add_argument('--tone', choices=['professional', 'casual', 'professional-friendly'],
                        default='professional-friendly')
    parser.add_argument('--length', choices=['short', 'medium'], default='short')
    
    # Output
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    parser.add_argument('--no-research', action='store_true', help='Skip website research')
    parser.add_argument('--provider', choices=['auto', 'openai', 'anthropic'], default='auto')
    
    args = parser.parse_args()
    
    # Build prospect
    prospect = Prospect(
        name=args.name,
        company=args.company,
        role=args.role,
        email=args.email,
        website=args.website
    )
    
    # Research
    if args.website and not args.no_research:
        print("Researching prospect...", file=sys.stderr)
        researcher = ProspectResearcher()
        prospect = researcher.research(prospect)
        if prospect.company_description:
            print(f"  Found: {prospect.company_description[:80]}...", file=sys.stderr)
    
    # Build config
    config = EmailConfig(
        sender_name=args.sender,
        sender_company=args.sender_company,
        value_prop=args.value_prop,
        cta=args.cta,
        tone=args.tone,
        length=args.length
    )
    
    # Generate
    try:
        generator = ColdEmailGenerator(args.provider)
        print(f"Generating with {generator.provider}...", file=sys.stderr)
        email = generator.generate(prospect, config)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Output
    if args.json:
        result = {'prospect': asdict(prospect), 'email': email}
        print(json.dumps(result, indent=2))
    else:
        print(format_email(email, prospect))


if __name__ == '__main__':
    main()
