import argparse
import os
import requests
import subprocess
import sys
import time
import urllib

from pathlib import Path
from setup_python import python_config as python_requirements

def download_file(url, filepath):
    path = filepath
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok = True)
            
    if (type(url) is list):
        for url_option in url:
            print("Downloading", url_option)
            try:
                download_file(url_option, filepath)
                return
            except urllib.error.URLError as e:
                print(f"URL Error encountered: {e.reason}. Proceeding with backup...\n\n")
                os.remove(filepath)
                pass
            except urllib.error.HTTPError as e:
                print(f"HTTP Error  encountered: {e.code}. Proceeding with backup...\n\n")
                os.remove(filepath)
                pass
            except:
                print(f"Something went wrong. Proceeding with backup...\n\n")
                os.remove(filepath)
                pass
        raise ValueError(f"Failed to download {filepath}")
    if not(type(url) is str):
        raise TypeError("Argument 'url' must be of type list or string")

    with open(filepath, 'wb') as f:
        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        response = requests.get(url, headers = headers, stream = True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            start_time = time.time()
            for data in response.iter_content(chunk_size = max(int(total / 1000), 1024 * 1024)):
                downloaded += len(data)
                f.write(data)
                
                try:
                    done = int(50 * downloaded / total) if downloaded < total else 50
                    percentage = (downloaded / total) * 100 if downloaded < total else 100
                except ZeroDivisionError:
                    done = 50
                    percentage = 100
                elapsed_time = time.time() - start_time
                try:
                    avg_kb_per_second = (downloaded / 1024) / elapsed_time
                except ZeroDivisionError:
                    avg_kb_per_second = 0.0

                avg_speed_string = '{:.2f} KB/s'.format(avg_kb_per_second)
                if (avg_kb_per_second > 1024):
                    avg_mb_per_second = avg_kb_per_second / 1024
                    avg_speed_string = '{:.2f} MB/s'.format(avg_mb_per_second)
                sys.stdout.write('\r[{}{}] {:.2f}% ({})     '.format('█' * done, '.' * (50-done), percentage, avg_speed_string))
                sys.stdout.flush()
    sys.stdout.write('\n')

def download_file_if_needed(url, path):
    if not Path(path).exists():
        print("Downloading {0:s} to {1:s}".format(url, path))
        download_file(url, path)

def download_special_source():
    javadoc = "SpecialSource-1.10.0-javadoc.jar"
    shaded = "SpecialSource-1.10.0-shaded.jar"
    sources = "SpecialSource-1.10.0-sources.jar"
    jar = "SpecialSource-1.10.0.jar"
    license = "SPECIAL_SOURCE_LICENSE"

    need_download = False
    if not Path(javadoc).exists():
        need_download = True
    if not Path(shaded).exists():
        need_download = True
    if not Path(sources).exists():
        need_download = True
    if not Path(jar).exists():
        need_download = True
    if not Path(license).exists():
        need_download = True

    if need_download:
        permission_granted = False
        while not permission_granted:
            reply = str(input("Would you like to download Special Source? [Y/N]: ")).lower().strip()[:1]
            if reply == 'n':
                return False
            permission_granted = (reply == 'y')

        download_file_if_needed("https://repo1.maven.org/maven2/net/md-5/SpecialSource/1.10.0/SpecialSource-1.10.0-javadoc.jar", javadoc)
        download_file_if_needed("https://repo1.maven.org/maven2/net/md-5/SpecialSource/1.10.0/SpecialSource-1.10.0-shaded.jar", shaded)
        download_file_if_needed("https://repo1.maven.org/maven2/net/md-5/SpecialSource/1.10.0/SpecialSource-1.10.0-sources.jar", sources)
        download_file_if_needed("https://repo1.maven.org/maven2/net/md-5/SpecialSource/1.10.0/SpecialSource-1.10.0.jar", jar)
        download_file_if_needed("https://raw.githubusercontent.com/md-5/SpecialSource/master/LICENSE", license)

    return True

def download_cfr():
    javadoc = "cfr-0.152-javadoc.jar"
    sources = "cfr-0.152-sources.jar"
    jar = "cfr-0.152.jar"
    license = "CFR_LICENSE"

    need_download = False
    if not Path(javadoc).exists():
        need_download = True
    if not Path(sources).exists():
        need_download = True
    if not Path(jar).exists():
        need_download = True
    if not Path(license).exists():
        need_download = True

    if need_download:
        permission_granted = False
        while not permission_granted:
            reply = str(input("Would you like to download CFR? [Y/N]: ")).lower().strip()[:1]
            if reply == 'n':
                return False
            permission_granted = (reply == 'y')

        download_file_if_needed("https://repo1.maven.org/maven2/org/benf/cfr/0.152/cfr-0.152-javadoc.jar", javadoc)
        download_file_if_needed("https://repo1.maven.org/maven2/org/benf/cfr/0.152/cfr-0.152-sources.jar", sources)
        download_file_if_needed("https://repo1.maven.org/maven2/org/benf/cfr/0.152/cfr-0.152.jar", jar)
        download_file_if_needed("https://raw.githubusercontent.com/leibnitz27/cfr/master/LICENSE", license)
    return True

def decompile_jar():
    try_again = True
    while try_again:
        jar_path = input("Please enter the path to the .jar file: ")
        if not Path(jar_path).exists():
            print(jar_path, "does not exist!")
            print("Please enter a existing jar file path")
            continue
        
        # Could be on internet or local + check if exists
        mappings = input("Please enter the url to the mappings file: ")
    
        absolute_jar_path = os.path.abspath(jar_path)
        jar_name = os.path.basename(absolute_jar_path)
    
        deobfuscated_path = f"decompiled_{jar_name}\deobfuscated_{jar_name}"
        decompiled_path = f"decompiled_{jar_name}\{jar_name}_source"
    
        print("Deobfuscating", jar_name, "...")
        special_source_str = f"java -cp SpecialSource-1.10.0.jar;*;. net.md_5.specialsource.SpecialSource --in-jar {absolute_jar_path} --out-jar {deobfuscated_path} --srg-in {mappings} --kill-lvt"
    
        subprocess.run(special_source_str)
    
        print("Decompiling", jar_name, "...")
        cfr_str = f"java -jar cfr-0.152.jar {deobfuscated_path} --outputdir {decompiled_path}"
        subprocess.run(cfr_str)
    
        print("Decompiling completed!")
        break

python_requirements.validate() # Confirm everything for the setup is installed

ss_success = download_special_source()
if not ss_success:
    print("Special Source is required!")

cfr_success = download_cfr()
if not cfr_success:
    print("CFR is required!")

decompile_jar()