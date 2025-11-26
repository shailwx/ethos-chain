# 🎤 Sentinel - Hackathon Pitch Guide

> **Critical:** This is the most critical part of the hackathon! A great presentation can win even if the code isn't 100% perfect.

---

## ⏱️ The 3-Minute Pitch Script

### 0:00 - 0:30 | The Hook (The Problem)

"Hi everyone, we are DNB.

We all want to buy ethical products. But for a large company, checking the ethics of 5,000 suppliers is impossible. It's a manual, slow process. Usually, companies only find out about forced labor or environmental dumping after the scandal hits the news and their stock price drops.

We need a way to audit suppliers 24/7, without an army of humans."

---

### 0:30 - 1:00 | The Solution (Sentinel)

"That's why we built **Sentinel**.

Sentinel is an AI-powered 'Ethics Watchdog'. It doesn't just Google things. It uses a **Multi-Agent Architecture** on AWS Bedrock.

We have a **Supervisor Agent** that manages the work. It sends an **Investigator Agent** to scour the web for news, and an **Auditor Agent** that reads our internal 'Code of Conduct' PDF to legally evaluate if a supplier is compliant or not."

---

### 1:00 - 2:00 | The Live Demo (Crucial!)

**(Switch screen to your Streamlit Dashboard)**

"Let me show you. Here is the Sentinel Dashboard.

Let's say I'm a procurement officer and I want to check on 'Acme Corp'. I type it in here...

**(Type name and click Audit)**

While this runs, here is what's happening: The Investigator is finding a recent news article about a chemical spill. The Auditor is reading our uploaded PDF policy, seeing that we have a 'Zero Tolerance' for pollution, and flagging this as a CRITICAL risk.

**(Results appear)**

And there it is. You see a **RED risk score**. But look at the evidence—it cites the specific source. It's transparent, instant, and actionable."

---

### 2:00 - 2:30 | Architecture & Impact

"We built this using **AWS Bedrock Agents** and **Claude 3.5 Sonnet**. We use a **Knowledge Base** for the policy documents, meaning you can swap the PDF to match any company's rules.

The impact? We move compliance from a yearly tick-box exercise to **real-time monitoring**. We protect the brand, and more importantly, we protect human rights."

---

### 2:30 - 3:00 | Closing

"In the future, we'll add real-time web scraping and blockchain verification.

Thank you. I'm happy to take questions."

---

## 🧪 Live Demo Checklist (Don't skip this!)

### Pre-Demo Setup
- [ ] **Pre-load the App**: Have `streamlit run app.py` running in your terminal before you walk on stage
- [ ] **Zoom In**: Press `Ctrl +` (or `Cmd +` on Mac) in your browser 2-3 times. Text is always too small on projectors
- [ ] **Clean Data**: Make sure your "Mock Data" (or the example you type in) definitely returns a result. Don't improvise the company name on stage

### The "Backup" Plan
- [ ] **Take a Screenshot**: Capture a successful audit result beforehand
- [ ] **If Demo Fails**: Switch to the screenshot immediately and say:
  > "The live Wi-Fi is slow, but here is the result from a run I did 5 minutes ago."
  
  *Judges respect the preparation.*

---

## 🎯 Q&A Prep: Anticipating Judge Questions

### Q: How do you prevent the AI from hallucinating fake news?

**A:** "That's why we use a **Multi-Agent approach**. The Investigator Agent is restricted to retrieving text from specific sources, and the Auditor Agent only evaluates that text. We also force the UI to display the citation link so a human can verify it."

---

### Q: Can this handle thousands of suppliers?

**A:** "Yes, the architecture is **serverless** using AWS Lambda and Bedrock. We could run this as a batch job overnight for 10,000 suppliers."

---

### Q: Why use Agents instead of just a simple RAG chain?

**A:** "Because compliance isn't linear. Sometimes the agent needs to 'go back' and look for more info if the first search was ambiguous. An **Agentic workflow** allows for that reasoning loop, whereas a simple chain does not."

---

## 🎬 Presentation Tips

### Body Language
- Stand confidently, make eye contact with judges
- Speak clearly and at a moderate pace
- Use hand gestures to emphasize key points (Multi-Agent Architecture, Real-Time Monitoring)

### Visual Flow
1. Start with you/team slide (optional)
2. Problem statement (show complexity)
3. Solution overview (architecture diagram)
4. **LIVE DEMO** (this is your moment!)
5. Technical details (AWS services)
6. Impact & business value
7. Future roadmap
8. Thank you + Q&A

### Energy Management
- **Start strong**: Hook them in the first 15 seconds
- **Peak energy during demo**: This is where you shine
- **End confident**: Strong closing statement

---

## 📋 Pre-Stage Checklist

### Technical
- [ ] Laptop fully charged + charger backup
- [ ] Internet connection tested (WiFi + mobile hotspot backup)
- [ ] Streamlit app tested and running smoothly
- [ ] Browser tabs organized (close unnecessary tabs)
- [ ] Demo data pre-loaded and verified
- [ ] Screenshot backup saved and accessible

### Presentation
- [ ] Slides loaded (if using any)
- [ ] Architecture diagrams ready to show
- [ ] HDMI/USB-C adapter tested with projector
- [ ] Clicker/remote tested (if provided)
- [ ] Water bottle nearby

### Mental
- [ ] Deep breath - you've got this!
- [ ] Remember: Judges want you to succeed
- [ ] Focus on the problem you're solving
- [ ] Be passionate about the impact

---

## 🚀 Final Pep Talk

**You have:**
- ✅ A solid multi-agent architecture
- ✅ A clear business case
- ✅ Real social impact
- ✅ Working AWS Bedrock implementation
- ✅ Comprehensive documentation

**Remember:**
- Judges love **passion** and **clarity**
- A working demo beats perfect code
- **Impact** (human rights + business value) = winning combination
- You're solving a real problem that affects millions

---

## 📞 Emergency Contacts

**If tech fails completely:**
- Pivot to architecture diagram discussion
- Walk through the JSON response structure
- Show the code structure in VS Code
- Emphasize the business case and impact

**Confidence statement if asked "Is this production-ready?":**
> "This is a working MVP that demonstrates the core concept. For production, we'd add monitoring, error handling, and scale testing. But the multi-agent architecture you see here is the foundation."

---

**Good luck, team! Go crush it!** 🚀

---

**Last Updated:** 2025-11-26  
**Event:** Oslo GenAI Hackathon 2025  
**Team:** Atif, Naresh, Shailendra
