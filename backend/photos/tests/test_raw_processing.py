import os
from pathlib import Path

from photos.utils.fs import download_file, md5sum
from photos.utils.raw import generate_jpeg, process_ensure_raw_processed_tasks, identified_as_jpeg


PHOTOS = [
    # -e argument to dcraw means JPEG was extracted without any processing
    ('Adobe DNG Converter - Canon EOS 5D Mark III - Lossy JPEG compression (3_2).DNG',  'dcraw -e', '1236950, 'https://raw.pixls.us/getfile.php/1023/nice/Adobe%20DNG%20Converter%20-%20Canon%20EOS%205D%20Mark%20III%20-%20Lossy%20JPEG%20compression%20(3:2).DNG'),
    ('Apple - iPhone 8 - 16bit (4_3).dng',                                              'dcraw -w', '772618, 'https://raw.pixls.us/getfile.php/2835/nice/Apple%20-%20iPhone%208%20-%2016bit%20(4:3).dng'),  # No embedded JPEG
    ('Canon - Canon PowerShot SX20 IS.DNG',                                             'dcraw -w', '1828344, 'https://raw.pixls.us/getfile.php/861/nice/Canon%20-%20Canon%20PowerShot%20SX20%20IS.DNG'),  # Embedded image but low resolution and not a JPEG
    ('Canon - EOS 7D - sRAW2 (sRAW) (3:2).CR2',                                         'dcraw -e', '2264602, 'https://raw.pixls.us/getfile.php/129/nice/Canon%20-%20EOS%207D%20-%20sRAW2%20(sRAW)%20(3:2).CR2'),
    ('Canon - Powershot SX110IS - CHDK.CR2',                                            'dcraw -w', '1493825, 'https://raw.pixls.us/getfile.php/144/nice/Canon%20-%20Powershot%20SX110IS%20-%20CHDK.CR2'),  # No embedded JPEG, No metadata about image dimensions for us to compare against
    ('Leica - D-LUX 5 - 16_9.RWL',                                                      'dcraw -w', '1478207, 'https://raw.pixls.us/getfile.php/2808/nice/Leica%20-%20D-LUX%205%20-%2016:9.RWL'),  # Less common aspect ratio, fairly large embedded JPEG but not similar enough to the raw's dimensions
    ('Nikon - 1 J1 - 12bit compressed (Lossy (type 2)) (3_2).NEF',                      'dcraw -e', '635217, 'https://raw.pixls.us/getfile.php/2956/nice/Nikon%20-%201%20J1%20-%2012bit%20compressed%20(Lossy%20(type%202))%20(3:2).NEF'),
    ('Sony - SLT-A77 - 12bit compressed (3_2).ARW',                                     'dcraw -w', '859814, 'https://raw.pixls.us/getfile.php/2691/nice/Sony%20-%20SLT-A77%20-%2012bit%20compressed%20(3:2).ARW'),  # Large embedded JPEG but not the right aspect ratio and smaller than raw
]


def test_extract_jpg():
    for fn, intended_process_params, intended_filesize, url in PHOTOS:
        raw_photo_path = str(Path(__file__).parent / 'photos' / fn)
        if not os.path.exists(raw_photo_path):
            download_file(url, raw_photo_path)

        output_path, process_params = generate_jpeg(raw_photo_path)

        assert process_params == intended_process_params
        assert identified_as_jpeg(output_path) == True
        filesizes = [intended_filesize, os.stat(output_path).st_size]
        assert min(filesizes) / max(filesizes) > 0.8  # Within 20% of the intended JPEG filesize

        os.remove(output_path)