from models import Card


CONVERSION = {
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10
}


def create_deck():
    """
    Create a list of playing cards in our database
    """
    suits = [0, 1, 2, 3]
    ranks = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace']

    def get_card_image(suit, rank):
        rank_repr = CONVERSION[rank] if rank in CONVERSION else rank

        suit_repr = ""
        for suit_index, suit_name in Card.SUITS:
            if suit == suit_index:
                suit_repr = suit_name
                break

        return "card_images/{}_of_{}s.jpg".format(rank_repr, suit_repr)

    cards = [Card(suit=suit, rank=rank, image=get_card_image(suit, rank)) for rank in ranks for suit in suits]
    Card.objects.bulk_create(cards)