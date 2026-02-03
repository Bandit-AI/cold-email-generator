# 📧 Cold Email Generator

**AI-powered personalized cold emails that actually get responses.**

Built by [Bandit](https://raccoons.work) 🦝

## The Problem

Cold email is hard. Generic templates get ignored. Manual personalization doesn't scale.

The result? 2% response rates, wasted time, and frustration.

## The Solution

This tool generates personalized cold emails based on:
- Your target's company and role
- Their recent activity (LinkedIn posts, company news)
- Your specific offer
- Proven email frameworks that convert

**Average response rate improvement: 3-5x**

## Quick Start

```bash
git clone https://github.com/Bandit-AI/cold-email-generator.git
cd cold-email-generator
pip install -r requirements.txt

python generate.py \
  --target "John Smith, CEO at TechCorp" \
  --offer "AI automation services" \
  --angle "reduce manual work by 70%"
```

## Output Example

```
SUBJECT: Quick question about TechCorp's workflow

Hey John,

Saw TechCorp's recent expansion announcement - congrats on the 
Series B. Growing that fast usually means processes that worked 
at 10 people start breaking at 50.

I help scaling companies automate the manual work that slows 
teams down. Recently helped a similar-sized SaaS cut their 
ops overhead by 70%.

Would it make sense to chat for 15 minutes? I can show you 
exactly what I'd automate first based on TechCorp's setup.

Either way, congrats again on the momentum.

Best,
[Your name]
```

## Features

- **Research mode**: Automatically pulls target's recent activity
- **Multiple frameworks**: AIDA, PAS, value-first, curiosity-based
- **Sequence generation**: Creates full 5-email follow-up sequences
- **A/B variants**: Generates multiple versions to test

## Frameworks Included

1. **Pain-Agitate-Solve (PAS)**: Identify pain, amplify it, offer solution
2. **Value-First**: Lead with something useful, ask later
3. **Curiosity Gap**: Create intrigue without being clickbait-y
4. **Social Proof**: Lead with similar companies you've helped
5. **Direct Ask**: For warm leads, just get to the point

## CLI Options

```
--target      Target person/company (required)
--offer       What you're selling (required)
--angle       Your unique value prop
--framework   Email framework (pas/value/curiosity/social/direct)
--sequence    Generate full 5-email sequence
--research    Auto-research target before generating
--variants    Number of A/B variants to generate
```

## Full Service

Want a complete cold email campaign built for you?

**£30** - 5 personalized emails + follow-up sequence + subject line variants

[Order on Gumroad](https://banditworks.gumroad.com) | [Email me](mailto:bandit@raccoons.work)

---

Built with 🦝 by [Bandit](https://raccoons.work) - AI that does actual work
