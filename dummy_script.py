import uuid
from faker import Faker
from extensions import db
from models.user import User  # Ganti dengan path ke model User Anda

# Inisialisasi Faker
fake = Faker()

# Fungsi untuk membuat dan menyimpan pengguna dummy
def insert_dummy_users(num_users):
    with db.session.begin():  # Memulai sesi dan memastikan commit otomatis
        for _ in range(num_users):
            user = User(
                id=uuid.uuid4(),  # Menghasilkan UUID baru
                username=fake.user_name(),
                email=fake.email(),
                age=fake.random_int(min=18, max=90),  # Usia acak antara 18 dan 90
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            db.session.add(user)  # Menambahkan pengguna ke sesi
    print(f'Successfully inserted {num_users} dummy users into the database.')

if __name__ == '__main__':
    # Jumlah pengguna dummy yang ingin dibuat
    insert_dummy_users(10)
