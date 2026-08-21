import shutil
import os

def static_to_public(static_path='static', public_path='public'):
    if os.path.exists(static_path):
        for entry in os.listdir(static_path):
            new_static_path = os.path.join(static_path, entry)
            new_public_path = os.path.join(public_path, entry)
    
            if os.path.isdir(new_static_path):
                os.mkdir(new_public_path)
                static_to_public(new_static_path, new_public_path)

            elif os.path.isfile(new_static_path):
                shutil.copy(new_static_path, new_public_path)
                print(f"created path: {new_public_path}")

def main(): #this should probably be in a separate script
    if os.path.exists('public'):
        shutil.rmtree('public')
        print('public was cleared')
    os.mkdir('public')
    print('made public dir')

    static_to_public()
main()