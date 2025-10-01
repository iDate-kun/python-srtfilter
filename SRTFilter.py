import os
import re

def read_prohibited_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        prohibited_words = [line.strip() for line in file]
    return prohibited_words

def search_prohibited_words_in_srt(srt_file, prohibited_words):
    with open(srt_file, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    found_prohibited_words = []
    for word in prohibited_words:
        # 部分一致で検索するために、\b（単語境界）を削除
        pattern = rf'(?i){re.escape(word)}'
        matches = re.finditer(pattern, srt_content)
        for match in matches:
            # タイムスタンプを取得
            preceding_text = srt_content[:match.start()]
            timestamps = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', preceding_text)
            if timestamps:
                found_prohibited_words.append(f"{word} [{timestamps[-1].replace(',', ':')}]")
    
    return found_prohibited_words

def main():
    input_folder = 'input'
    srt_files = [f for f in os.listdir(input_folder) if f.endswith('.srt')]

    # エラーチェック
    if len(srt_files) == 0:
        print("エラー: srtファイルが見つかりません。")
        return

    prohibited_words = read_prohibited_words('prohibited_words.txt')

    for srt_file in srt_files:
        srt_file_path = os.path.join(input_folder, srt_file)
        found_words = search_prohibited_words_in_srt(srt_file_path, prohibited_words)
        
        if found_words:
            print(f"{srt_file}")
            for word in found_words:
                print(word)
            print("\n")  # 次のsrtファイルとの区切りのために1行空ける
        else:
            print(f"{srt_file}に禁止語句はありません\n")

if __name__ == "__main__":
    main()


