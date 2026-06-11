# ***Agent Personalization: an agent that knows you***

**PerDate:** April 28, 2026

**Author: Apoorva Shete**

Agent Personalization tailors every response the agent gives you. Instead of treating every user the same, Falconer builds a lightweight profile of who you are, captured as a set of **attributes** like your role, your team, the systems you own, the projects you care about, and uses them to tailor answers and skip context you already know. Your attributes are yours: you can see every one, edit it, or remove it.

**What is an attribute?**

Attributes come from two sources:

- **Attributes you add:** facts you write directly in your profile: your role, your team, and personal preferences like “I prefer bullet points over tables.”
- **Auto-detected attributes**: facts Falconer extracts from your Slack and in-app conversations as you use the product. Each one is traced back to its source so you can verify it.

Every attribute is reviewable from a single page. You can filter by “added by you” vs. “auto-detected,” search across attributes, edit any one inline, or delete what you don’t want Falconer to use.

**How it works**

As you interact with Falconer, the system:

1\. Observes your conversations across Slack and the Falconer app

2\. Extracts durable, identity-level attributes (not one-off questions or transient context)

3\. Traces each one back to its source so you can verify it

4\. Injects relevant attributes into the agent’s system prompt at query time

5\. Lets you correct or remove any attribute that’s wrong or outdated

**Control and Customization**

Your profile is editable end-to-end. Add a role and team in one click. Add a freeform attribute up to 500 characters. Edit any auto-detected attribute. Once you do, it’s marked “Edited by you” and Falconer trusts your version. Delete anything you’d rather Falconer forget.

**Why this matters**

- Agent answers tuned to your role and ownership area, not a generic default
- Less repetitive setup: you don’t re-explain your team or scope on every query
- Full transparency: every attribute is visible, attributed, and reversible
- Profile improves passively as you use the product, with no extra effort

**Best Use cases**

- Engineers and PMs who want answers scoped to the services they own, not the whole codebase
- Non-technical stakeholders who need plain-language summaries, not implementation details
- Writers and PMs who prefer a specific style (no em dashes, shorter sentences, bullet points over prose)
- Cross-functional teams where the same question means something different depending on the role asking it
- Power users who want the agent to skip onboarding-level context and get straight to the point

**Try it today**

Agent Personalization is available now under your personal settings. Visit Settings → Personalizations → Agent Personalization to review your attributes.

## **LinkedIn post**

Most AI agents only know what you’ve told them directly. So you spend half your prompts re-explaining your team, your stack, the project codenames nobody outside your company would understand.

Falconer’s new Agent Personalization feature closes that gap by learning from where you actually work. It builds a profile of you from your Slack and in-app conversations: your role, your team, the systems you own, how you like answers formatted. The agent shows up already knowing the context you’d otherwise have to paste in every time.

Every attribute is sourced, editable, and reversible. Your profile is yours.

Falconer is an organizational brain for your team. Personalization is what turns it from a shared search bar into something that actually knows you.

## **X post**

Most AI agents treat everyone the same.

Falconer doesn’t. It learns your role, your team, the systems you own, and how you like answers formatted, all from your actual conversations in Slack and the app.

No more re-explaining context every time you ask a question.

Every attribute is visible, editable, and reversible. Your profile is yours.

Agent Personalization: an agent that actually knows you.

### Updates

Testing updates via github webhook
