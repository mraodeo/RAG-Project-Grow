import os
import re
import glob

def clean_text(text):
    # Split into lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # 1. Remove boilerplate (nav menus, footers, etc.)
    # Groww's boilerplate usually ends around "Login/Sign up" or "Search Groww"
    start_idx = 0
    for i, line in enumerate(lines):
        if "Login/Sign up" in line or "Search Groww" in line:
            start_idx = i + 1
            
    # And it usually has a footer starting around "Mutual Funds" -> "Mutual Fund Houses" -> "AMC"
    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        if "Mutual Fund Houses" in line or "About Groww" in line or "Groww address" in line or "Privacy Policy" in line:
            end_idx = i
            break
            
    lines = lines[start_idx:end_idx]
    
    # 2. Extract key facts and add headers
    cleaned_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip some weird UI artifacts (like individual numbers for the animated counter)
        if re.match(r'^[\d\.\+\%]$', line):
            i += 1
            continue
            
        # Add section headers for known keys
        keys_to_format = [
            "Expense ratio", "Exit load", "Min. for SIP", "Fund size (AUM)", 
            "NAV", "Benchmark", "Lock-in", "Riskometer", "Fund manager", "Launch date"
        ]
        
        matched_key = None
        for key in keys_to_format:
            if line.lower().startswith(key.lower()):
                matched_key = key
                break
                
        if matched_key and i + 1 < len(lines):
            # This is a key-value pair separated by newline in the raw text
            cleaned_lines.append(f"**{matched_key}**: {lines[i+1]}")
            i += 2
            continue
            
        # For inline key-value or normal text
        cleaned_lines.append(line)
        i += 1

    # 3. Deduplicate consecutive identical lines
    deduped = []
    for line in cleaned_lines:
        if not deduped or deduped[-1] != line:
            deduped.append(line)
            
    # 4. Remove marketing/generic language (basic regex)
    marketing_phrases = ["Invest now!", "Start your journey", "Buy now, pay later", "Begin your stock market journey"]
    final_lines = []
    for line in deduped:
        if not any(phrase.lower() in line.lower() for phrase in marketing_phrases):
            final_lines.append(line)
            
    return "\n".join(final_lines)

def main():
    raw_dir = os.path.join("data", "raw")
    proc_dir = os.path.join("data", "processed")
    
    os.makedirs(proc_dir, exist_ok=True)
    
    # Process each scheme directory
    for scheme_dir in glob.glob(os.path.join(raw_dir, "*")):
        if os.path.isdir(scheme_dir):
            scheme_slug = os.path.basename(scheme_dir)
            raw_file = os.path.join(scheme_dir, "scheme_info.txt")
            
            if os.path.exists(raw_file):
                print(f"Cleaning {scheme_slug}...")
                with open(raw_file, "r", encoding="utf-8") as f:
                    raw_text = f.read()
                    
                cleaned_text = clean_text(raw_text)
                
                # Save to processed directory
                out_path = os.path.join(proc_dir, f"{scheme_slug}.txt")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(cleaned_text)
                    
                print(f"  Saved {out_path} ({len(cleaned_text)} characters)")

if __name__ == "__main__":
    main()
