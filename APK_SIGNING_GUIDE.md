# 🔐 Secure APK Signing Guide

## Create Secure Keystore

```bash
# Create a secure keystore (do this ONCE and keep safe!)
keytool -genkey -v -keystore maya-chatbot-key.keystore -alias maya-chatbot -keyalg RSA -keysize 2048 -validity 10000

# You'll be prompted for:
# - Keystore password (use strong password)
# - Key password (use strong password)  
# - Your details (name, organization, etc.)
```

## Update buildozer.spec for Signing

Add to buildozer.spec:
```ini
[buildozer]
# Path to your keystore
android.keystore = maya-chatbot-key.keystore

# Alias name
android.keyalias = maya-chatbot

# These will be prompted during build
# android.keystore_passwd = 
# android.keyalias_passwd = 
```

## Build Signed APK

```bash
# Build release APK (will prompt for passwords)
buildozer android release

# Verify APK signature
jarsigner -verify -verbose -certs bin/malaychatbot-1.0.0-release.apk
```

## Security Best Practices

1. **Keep Keystore Safe**: 
   - Store in secure location
   - Backup keystore file
   - Never share keystore passwords

2. **Use Strong Passwords**:
   - Minimum 12 characters
   - Mix of letters, numbers, symbols
   - Different passwords for keystore and key

3. **APK Verification**:
   - Always verify signature before distribution
   - Check APK with antivirus tools
   - Test on clean devices

4. **Distribution Security**:
   - Use HTTPS for downloads
   - Provide SHA256 checksums
   - Monitor for unauthorized modifications

## Emergency Response

If keystore is compromised:
1. Stop all distribution immediately
2. Create new keystore with different passwords
3. Build and redistribute new APK
4. Notify users of security update
