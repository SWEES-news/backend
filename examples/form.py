"""
This module provides the glossary query form
"""

import examples.form_filler as ff

from examples.form_filler import FLD_NM  # for tests

USERNAME = 'username'
PASSWORD = 'password'

PARTY = 'party'
COUNTRY = 'country'
AGE = 'age'

SURVEY_FORM_FLDS = [
    {
        FLD_NM: 'Instructions',
        ff.QSTN: 'Enter your political party and country of residence',
        ff.INSTRUCTIONS: True,
    },
    {
        FLD_NM: PARTY,
        ff.QSTN: 'Political Party:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        FLD_NM: COUNTRY,
        ff.QSTN: 'Country:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        FLD_NM: AGE,
        ff.QSTN: 'Age: ',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
]


def get_form() -> list:
    return SURVEY_FORM_FLDS


def get_form_descr() -> dict:
    """
    For Swagger!
    """
    return ff.get_form_descr(SURVEY_FORM_FLDS)


def get_fld_names() -> list:
    return ff.get_fld_names(SURVEY_FORM_FLDS)


def main():
    # print(f'Form: {get_form()=}\n\n')
    print(f'Form: {get_form_descr()=}\n\n')
    # print(f'Field names: {get_fld_names()=}\n\n')


if __name__ == "__main__":
    main()
