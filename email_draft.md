# Email Draft to SpeechSuper API Support

**Subject**: API Integration Issue - Invalid coreType Error (App ID: 175152606100052e)

---

**To**: SpeechSuper API Support Team  
**From**: [Your Name]  
**Date**: [Current Date]

Dear SpeechSuper Support Team,

I hope this email finds you well. I am currently integrating the SpeechSuper Pronunciation Assessment API into a Korean language learning application and am experiencing persistent issues with coreType validation.

## Issue Summary
I am consistently receiving "invalid coreType" errors (Error ID: 41030) for ALL core types that are documented in your API samples and documentation. This issue has persisted across multiple testing sessions and appears to have worsened recently.

## Technical Details
- **Application ID**: 175152606100052e
- **API Endpoint**: https://api.speechsuper.com/
- **Audio Format**: WAV, 16kHz, 16-bit, mono
- **Integration Method**: HTTP POST with proper authentication signatures
- **Timestamp Format**: Milliseconds (matching WebSocket samples)

## Core Types Tested (ALL Currently Failing)
I have tested the following core types from your official documentation, and ALL now return "invalid coreType" errors:

### Single Word Evaluation:
- `word.eval.promax` ❌
- `word.eval` ❌

### Sentence Evaluation:
- `sent.eval` ❌
- `sent.eval.promax` ❌ (was working earlier today)
- `para.eval` ❌

## Timeline of Issues
- **Earlier Today**: `sent.eval.promax` was working and returning detailed pronunciation scores
- **Current Status**: ALL core types now return "invalid coreType" error
- **Possible Cause**: Account access changes, rate limiting, or server-side configuration changes

### Sample Error Response:
```json
{
  "error": "invalid coreType",
  "errId": 41030,
  "applicationId": "175152606100052e",
  "params": {
    "request": {
      "coreType": "word.eval.promax",
      "refText": "namja",
      "tokenId": "tokenId"
    }
  }
}
```

## Urgent Questions
1. **Has there been any change to my account access or permissions?**
2. **Are there any rate limiting policies that could cause complete API failure?**
3. **Which core types are actually supported for my application ID?**
4. **Are there any account-level restrictions on core types that I should be aware of?**
5. **Do I need to enable specific features or upgrade my account to access certain core types?**
6. **Is there a way to query available core types programmatically?**

## Request for Immediate Assistance
This is blocking development of a language learning application. Could you please:
1. **Verify my account status and any recent changes**
2. **Provide a list of valid core types for my application ID**
3. **Check if there are any server-side issues affecting my account**
4. **Confirm if any account configuration is needed**

I would greatly appreciate your assistance in resolving this issue. Please let me know if you need any additional information or logs.

Thank you for your time and support.

Best regards,
[Your Name]
[Your Email]
[Your Company/Organization (if applicable)]

---

**Attachments**:
- Full error logs (if needed)
- Sample audio file (if requested)
