from src.card_processing import card_operations, top_transactions


def test_card_operations():
    assert type(card_operations()) == list
    assert len(card_operations()) != 0
    assert card_operations() == [{'cashback': 2319.35, 'last_digits': 7197, 'total_spent': 2319346.86},
 {'cashback': 14.92, 'last_digits': 5091, 'total_spent': 14918.16},
 {'cashback': 545.26, 'last_digits': 4556, 'total_spent': 545261.72},
 {'cashback': 46.21, 'last_digits': 1112, 'total_spent': 46207.08},
 {'cashback': 84.0, 'last_digits': 5507, 'total_spent': 84000.0},
 {'cashback': 69.2, 'last_digits': 6002, 'total_spent': 69200.0},
 {'cashback': 470.85, 'last_digits': 5441, 'total_spent': 470854.8}]


def test_top_transactions():
    assert type(top_transactions()) == list
    assert len(top_transactions()) != 0
    assert top_transactions() == [{'amount': '152500.0',
  'category': 'Образование',
  'date': '18.01.2019',
  'description': 'СКОЛКОВО'},
 {'amount': '152500.0',
  'category': 'Образование',
  'date': '15.02.2019',
  'description': 'СКОЛКОВО'},
 {'amount': '152500.0',
  'category': 'Образование',
  'date': '19.09.2018',
  'description': 'СКОЛКОВО'},
 {'amount': '152500.0',
  'category': 'Образование',
  'date': '02.12.2018',
  'description': 'СКОЛКОВО'},
 {'amount': '100000.0',
  'category': 'Наличные',
  'date': '03.05.2019',
  'description': 'Операция в других кредитных организациях VB24 MOSKVA G RUS'}]