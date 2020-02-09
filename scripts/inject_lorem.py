import pandas
import numpy
from faker import Faker
from faker.providers import lorem
from pathlib import Path
from functools import partial

fake = Faker()  # generates fake data includes lorem
fake.add_provider(lorem)

LOREM = "Phasellus vitae fringilla lectus, sed laoreet dui. Aliquam facilisis lacus justo, eu fringilla lacus mollis vitae. Sed eget lorem egestas, malesuada magna ut, mattis felis.".split()


def bullets(num_bullets, words_per):
    return "\n".join(
        fake.sentence(nb_words=words_per, ext_word_list=LOREM, variable_nb_words=False)
        for _ in range(num_bullets)
    )


paragraph = partial(
    fake.paragraph, ext_word_list=LOREM, nb_sentences=6, variable_nb_sentences=True
)
word = partial(fake.word, ext_word_list=LOREM)

if __name__ == "__main__":
    # url data for tarot_card_image field, dict(id:url)
    IMGUR = {
        2: "https://i.imgur.com/OWFv2l5.jpg",
        18: "https://i.imgur.com/WSju3NU.jpg",
        8: "https://i.imgur.com/RIjxAh0.jpg",
        22: "https://i.imgur.com/aVYxJ9k.jpg",
        1: "https://i.imgur.com/3t5OZ95.jpg",
        12: "https://i.imgur.com/BzXabA5.jpg",
        7: "https://i.imgur.com/RU5dusE.jpg",
        5: "https://i.imgur.com/WxuFI1E.jpg",
        17: "https://i.imgur.com/2zKPo0E.jpg",
        14: "https://i.imgur.com/To8PXjL.jpg",
        6: "https://i.imgur.com/8JpuOOC.jpg",
        20: "https://i.imgur.com/ZxSKw3T.jpg",
        13: "https://i.imgur.com/xHOtAuQ.jpg",
        4: "https://i.imgur.com/F4IyE5l.jpg",
        11: "https://i.imgur.com/HVgn6Jg.jpg",
        3: "https://i.imgur.com/ph1uA6K.jpg",
        10: "https://i.imgur.com/L4TIBCx.jpg",
        19: "https://i.imgur.com/hBF4bFS.jpg",
        21: "https://i.imgur.com/RrAlqRf.jpg",
        16: "https://i.imgur.com/6T1hTDa.jpg",
        15: "https://i.imgur.com/8AMB8KX.jpg",
        9: "https://i.imgur.com/JSr4wbA.jpg",
    }
    table_name = "generators_generator"
    CSV_SRC_BARE = "./generators.csv"

    field_types = {
        "title": numpy.object,
        "number": numpy.int64,
        "tarot_card_image": numpy.object,
        "tarot_card_thumbnail": numpy.object,
        "astrological": numpy.object,
        "alchemical": numpy.object,
        "intelligence": numpy.object,
        "hebrew_letter": numpy.object,
        "letter_meaning": numpy.object,
        "watchtower_position": numpy.int64,
        "slashdot_position": numpy.int64,
        "description": numpy.object,
        "description_bullets": numpy.object,
        "galileo_content": numpy.object,
        "galileo_bullets": numpy.object,
        "f_loss_content": numpy.object,
        "f_loss_bullets": numpy.object,
        "st_paul_content": numpy.object,
        "st_paul_bullets": numpy.object,
    }

    fields = "id,title,number,tarot_card_image,astrological,alchemical,intelligence,hebrew_letter,letter_meaning,description,galileo_content,f_loss_content,st_paul_content,f_loss_bullets,galileo_bullets,st_paul_bullets,description_bullets,slashdot_position,watchtower_position,title_y,tarot_card_thumbnail".split(
        ","
    )
    bullet_fields = [
        "description_bullets",
        "galileo_bullets",
        "f_loss_bullets",
        "st_paul_bullets",
    ]
    full_fields = ["galileo_content", "f_loss_content", "st_paul_content"]
    single_fields = "astrological,alchemical,intelligence,hebrew_letter,letter_meaning".split(
        ","
    )

    cards = pandas.read_csv(CSV_SRC_BARE, dtype=field_types, keep_default_na=True)
    for index, card in cards.iterrows():
        for column in cards.columns:
            if pandas.isna(card[column]):
                if column in bullet_fields:
                    generator = partial(bullets, 6, 3)
                elif column in full_fields:
                    generator = paragraph
                elif column in single_fields:
                    generator = word
                elif column == "tarot_card_image":
                    generator = partial(IMGUR.get, card["id"])
                else:
                    continue
                cards.at[index, column] = generator()
    cards.to_csv(f"{table_name}.csv", index=False)
