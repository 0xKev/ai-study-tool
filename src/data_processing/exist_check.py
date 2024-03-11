# checks hash of file before uploading - only save uploaded hash to database once vectors are succesfully uploaded otherwise only half uploaded yet hash saved
import hashlib
import csv
import os.path

def get_hash(file: str) -> str:
    BUF_SIZE = 65536 # fixed buffer size, 65536 bytes

    md5 = hashlib.md5()

    with open(file, "rb") as f:
        while True:
            # read size = BUF_SIZE, store in data
            data = f.read(BUF_SIZE)

            # if eol - data = -1
            if not data:
                break
        
        # pass data read to md5
        md5.update(data)

    # returns hashed data (hexdigest) for visual representation
    return md5.hexdigest()


def save_hash(user_id: str, hash: str) -> None:
    csv_file_path = "D:/Documents/Coding/My projects/ai-study-tool/src/data/text_hashes.csv"
    csv_not_exists = not os.path.isfile(csv_file_path)
    header = ["user_id;hash"]
    row = [f"{user_id};{hash}"]

    '''
    - read and check if row in reader
    - if not then open file as writer and write then break
    - if yes then skip
    - head writer if csv_exist false
    '''
    if csv_not_exists:
        with open(csv_file_path, "w+", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

    with open(csv_file_path, "r+", newline="") as csvfile: # set as read mode for reader to function
        reader = csv.reader(csvfile)
        
        if row not in reader:
            with open(csv_file_path, "a", newline="") as csvfile: # 
                writer = csv.writer(csvfile)
                reader = csv.reader(csvfile)

                writer.writerow(row)


def is_file_uploaded(user_id: str, file_md5_hash: str) -> bool:
    # check against file hash csv file (user_id; file_hash) 
    # prefer above instead of running a separate search on vector database for performance reasons
    csv_file_path = "D:/Documents/Coding/My projects/ai-study-tool/src/data/text_hashes.csv"
    is_exist: bool = False
    user_row: str = f"{user_id};{file_md5_hash}"

    with open(csv_file_path, "r") as csvfile:
        reader: csv = csv.reader(csvfile)
        all_hashes: list = ["".join(hashes) for hashes in reader][1::]
        #print("all hashes:", all_hashes)
        
        if user_row in all_hashes:
            is_exist = True
        
        print("File already exists under user id:", user_id)
        #print(all_hashes)

    return is_exist



if __name__ == "__main__":
    #file1: str = get_hash("D:\Documents\Coding\My projects/ai-study-tool\pdf_files\The_Happy_Prince by Oscar Wilde.pdf")
    #print(f"file1 hash: {file1}")
       
    #save_hash("kevin", "d41d8cd98f00b204e9800998ecf8427e")
    print(is_file_uploaded("kevin", "d41d8cd98f00b204e9800998ecf8427e"))