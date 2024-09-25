
# Text Image Retrieval

abc



## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Once you have setup, you need to prepare the data folder :

![alt text](https://lh3.googleusercontent.com/fife/ALs6j_FETe8kv_AHLGFcIq39cFf4p2F286SnLB_AmbBzFIooSl_AKWhZwYSxJZmDVcOSea7WRDG9VhdhdjM2Z7nJ4I4bTGW6_Ug6ZVOsOyXPIAl54KR_jtxvalcD9MpvKTY_qmjZ8uqYgz6XxFaGpGHMytk_seD_bVNrRCxffYd-apnAnHoGb1fyFD2v1B5rIjY5pB5gAOVUyG_WnM8K6mr535w9URVuKtVZH5jVmXajGMPXpw-U64Y8HHsTWOYULCTOra276aQ5v6fSmvAbprhY2Wg25YwJKQmf31BqPI8pyvoBaI_2ReS65XhZCBGZz2P5KizjQ32cnJOs3JjsmrBjGuXhiVbwp1iGGGDws-STsDgHTvTgZ2PjLMFyp78AbQpIuVauslyWL4Hn2EN3xoGZmC-TZTTXUjpQJgqWtml3iFonOfj7aWwC6v0buRFYzNHfBQLHTPHT8TltN-QZ2iLzFu3Nnepq0-9cUbD8Mv3x3RmHFa-2nvpWqEUE3MnU8mRiAEn4-VOxFSGKTWyBRe6x30AzgdmE0elpKBCfkfUjkNpgYjU71RgIWxadPDaErQxtUkBHzLeEQnd4sSTthWX_zv51Qkr9RLKCgj5VyetqRJfRaMqHnPlrzjFHuUSO7s_OZdHuD5siQTGXV9tNTjOhemiHS5TPlcC2J151mxqRpSx4xHzl2PfuRaGaDJ6qXE2DR_GJC7NnOsDf2uo3tTPfIiqk3o6D9_qLFENjM7CuaoxVX37C8pqUZ2vo0FxxEFGy6c1JurSwjUYskiNuHeHDSJfqQbIzXM_JGbHzHWtA_RqHloety_d6CrcPHWMbx3bZ4X8MGbngl8yKhwE0znPqLaPR0x2Lqmk_eGZyMhMC9mXSXqzZ7HRs-vVdLDoglT87bmp5Xw1AUOzn8yJj7UlsIPy8EFiY77z0pHEpIxiyUqFiNl2PDl0OpE_8gH1XhGCgfaLDPk5MVdJq77RsNdXo51WOqmOUSd9NM7qebKIykO1uK3jI5DTUdxMVd_9dg-kZRopSRBH_NrlTjGxfP3THRF3Qw9EY6Lwd6kKxne-b1PovMNJ2nRwbqoc8GEO7U5QaZOhPgn4PzbbwvAATwAi8G2wHd1aN2ds2CiFkqe1idFnESY4Hqfl7kkBuZ6wUfEokPTcfpm5T-i7wNpwWh4XI8VBp7HR3nT7_CA85SfhqSSsdps4m31LkB9i0zoznV2R9EnfY7GI_yOFBuWrRXvA4IZGvOBzZIJWhVySa9dVo0Jrmz20YRQPGhP077MstUfRPiOQ7rjNoTYtYy_6BVg9eHzXj5CP6nzfl-IMwBstvU0GxA1Ggykm3hfgbrBMa_CoRoKsQ09ZKaS-ojHsMpkAz627G9axUpB1D6STmJKsodiF2ePzbTlhcbl97g-FWOyCEi1cSw4MhSaPTr4odZ4cjD7JHJupQt0SIZTnXNxuSCO0Y_t0KD0AQrWroFlz9NfUshg4UX3aokgZbGwLDHERimwzL1tiX69lRH5CxZ1349km1BkjDpJAQSq66l-L_ZITd0-19lUUQY7n50UfV-9DYpukZC_KqEKREvhWXMfliGzFsarvDyHLDp24n0_okqQmLN_aKFNmsuGH53z-6h5OpSA=w2561-h1219)

## Setup and Running `create_images_db.py`

This script is used to set up the ChromaDB and process the training dataset.

### 1. Set Up Directory Paths

Before running the script, ensure you have the following directories set up on your system:

- **Training Dataset**: Store your images in the directory specified by the `ROOTS` variable.
- **Database Path**: The ChromaDB database will be stored in the directory specified by the `db_path` variable.

### 2. Update the Script

Open `create_images_db.py` and update the following variables:

```python
# Path to your training dataset
ROOTS = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\data\data_image\train"

# Path to where the ChromaDB will be created/stored
db_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\database\database_image"


```
Initialize and embedding vector in chroma database

```bash
  python create_images_db.py
```

## Run streamlit

```bash
  streamlit run main.py
```

