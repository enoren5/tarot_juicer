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
        fake.sentence(nb_words=words_per, ext_word_list=LOREM,
                      variable_nb_words=False)
        for _ in range(num_bullets)
    )


paragraph = partial(
    fake.paragraph, ext_word_list=LOREM, nb_sentences=6, variable_nb_sentences=True
)
word = partial(fake.word, ext_word_list=LOREM)

if __name__ == "__main__":
    # url data for tarot_card_image field, dict(id:url)
    IMGUR = {
        3: "https://i.imgur.com/OdRnGXo.jpg",
        19: "https://i.imgur.com/70Bdg9W.jpg",
        9: "https://i.imgur.com/mo9aYsa.jpg",
        1 "https://i.imgur.com/VZx2NYe.jpg",
        2: "https://i.imgur.com/jR9VPO7.jpg",
        13: "https://i.imgur.com/bMo96Zf.jpg",
        8: "https://i.imgur.com/jl3Xpmt.jpg",
        6: "https://i.imgur.com/7MznbMZ.jpg",
        18: "https://i.imgur.com/XZMeAN9.jpg",
        15: "https://i.imgur.com/nWDto9M.jpg",
        7: "https://i.imgur.com/jcXqYAm.jpg",
        21: "https://i.imgur.com/Xyau2sI.jpg",
        14: "https://i.imgur.com/6dK2mqg.jpg",
        5: "https://i.imgur.com/tg23Z5v.jpg",
        12: "https://i.imgur.com/ESLajF3.jpg",
        4: "https://i.imgur.com/xnXciN8.jpg",
        11: "https://i.imgur.com/404NCcZ.jpg",
        20: "https://i.imgur.com/14mLbvD.jpg",
        22: "https://i.imgur.com/bQcaX5v.jpg",
        17: "https://i.imgur.com/1M1RezN.jpg",
        16: "https://i.imgur.com/K8qXjZA.jpg",
        10: "https://i.imgur.com/pvJTf0V.jpg",
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

    cards = pandas.read_csv(
        CSV_SRC_BARE, dtype=field_types, keep_default_na=True)
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
