# Redesign notes

A first pass at a re-imagined missteamaven.com. All the words, photos, reviews and logos come from the current site. The new copy you wrote recently (the league, individual, junior, coaches and neurodivergence pages) is strong, so most of it is kept nearly word for word and given a better stage.

## The idea

**Elite athlete + data nerd, in one look.** The current site says "unapologetic data nerd" but looks like a generic template. The new design leans into both halves:

- **Athlete:** big condensed sports type, full-bleed action photos, the derby track outline as a recurring graphic, jersey 1706.
- **Data nerd:** a monospaced "stat sheet" voice for labels, a scoreboard of the competitive record, and a sample performance dashboard that shows leagues what that service actually looks like.
- **Colors:** the navy and electric blue from the current site, plus a volt green used only for buttons and highlights, so the next step is always obvious.

## What's new

**Clearer structure.** Visitors pick who they are, then land on one page made for them:

| New page | Replaces |
|---|---|
| Home | Home + Coaching overview |
| Leagues (includes Bootcamps + FAQ) | Coaching Clinic, Bootcamps |
| Skaters | Individual Coaching |
| Juniors | "Consulting" (it was actually the junior page) |
| Coaches | Coaching the Coaches |
| Neurodivergence | "copy-of-coaching-the-coaches" |
| About (bio, record, teams, gallery) | About Me |
| Reviews (all 15) | Testimonials |
| Contact (form + calendar) | Contact, Upcoming Events |

Old links keep working: every old URL redirects to its new page.

**One call to action everywhere: the free intake chat.** It was your best hook and it was buried. Now it's in the header, the hero, and the end of every page.

**Smarter contact form.** Visitors tick what they're interested in (league training, bootcamp, juniors, and so on), add league, location and timeframe. Coming from the Juniors page pre-selects "Junior coaching", and so on. You'd get better-prepared first messages.

**Client logos you can actually read.** The current site shows acronyms (GGRD, BTDD, NYSE...). The new one shows the real logos as a clean wall.

**The record up front.** WFTDA champion 2014, 7 Championship podiums, World Cup bronze with England, World Cup MVP Team, Comeback Athlete of the Year. On the current site these sit low on the About page.

**Fast and phone-first.** Images went from about 42 MB of originals to about 3 MB, with no Wix scripts. It works at phone width with a full-screen menu.

## Fixed along the way

- Wix template placeholder text on the About page ("I'm a paragraph. Double click me...") under Branding, Storytelling, Design and Consulting. Removed.
- The Bootcamps and Coaching overview pages still had older copy pointing to an "Online Consulting" page that no longer exists. Merged into the new pages.
- Home "For coaches & events" card linked to the junior page and had a double bullet.
- Typos: "Testamonials", "Comback", "more then".
- Divergence Roller Derby was listed twice in the teams list.
- The Events page only showed one event, which is now in the past.
- Twitter/X link dropped (Instagram, Facebook and YouTube kept). Easy to add back.

## Please check these

1. **Review quotes** were lightly cleaned up (typos, and a few long ones trimmed with "..." on the home and service pages). Full versions are on the Reviews page. Happy to restore exact wording.
2. **"Past work includes Gotham Girls Junior Derby and Canada Junior Roller Derby"** on the Juniors page. I inferred that from the client logos. Is it right?
3. **"24 leagues, camps & events coached"** counts the logos on the current site. Is the real number higher?
4. **The client list:** I read "NYSE" as New York Shock Exchange and "JRD" as Jacksonville. Correct?
5. **The sample dashboard** numbers are made up and labeled "Sample". If you have a real (anonymized) example, it would be even better.
6. **"What happens next"** on the Contact page says the plan is custom with no standard packages. OK?

## Open questions

- **Junior photos.** There aren't any on the current site, so the Juniors page uses a team huddle shot. A real junior photo (with permission) would help a lot.
- **A newer headshot?** The portrait is in a Gotham kit. Something in Denver or England colors would match the current story.
- **The calendar.** Do you want clinics and bootcamps listed there, or would "ask about availability" be better than a list that goes stale?
- **Platform.** This is a plain static site, which is fast and free to host (Cloudflare Pages or similar), but editing means changing files rather than clicking in an editor. If you'd rather keep editing it yourself in Wix, we can rebuild this design inside Wix instead.
- **Contact form delivery.** Right now it opens the visitor's email app with the message pre-filled. Before launch it should send directly (a form service or a small serverless function), so nobody has to have email set up.
