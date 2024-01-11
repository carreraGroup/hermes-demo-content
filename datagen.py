## VERSION 2
import pandas as pd
import numpy as np
from pathlib import Path
import uuid
import csv
import datetime
import random
import string
import sys

rng = np.random.default_rng()

gender_choices = ['male', 'female']
active_choices = ['active', 'inactive']
finished_choices = ['finished', 'other']
completed_choices = ['completed', 'inactive']


#Patient needs a gender column. it can be male of female (female is in the measure)
#def random_gender():
#    return "male" if random.choice([True, False]) else "female"

#def random_active():
#    return "active" if random.choice([True, False]) else "inactive"

#def random_finished():
#    return "finished" if random.choice([True, False]) else "other"

#def random_completed():
#    return "completed" if random.choice([True, False]) else "other"

#def random_date_before(given_date, days_range=365):
#    """
#    Generates a random date before the given date.
    
#    :param given_date: The date before which to generate a random date.
#    :param days_range: The range of days before the given_date to consider for generating a random date.
#    :return: A random date before the given_date.
#    """
#    random_days = datetime.timedelta(days=random.randint(1, days_range))
#    return given_date - random_days

#def random_date_after(given_date, days_range=365):
#    """
#    Generates a random date after the given date.
    
#    :param given_date: The date after which to generate a random date.
#    :param days_range: The range of days after the given_date to consider for generating a random date.
#    :return: A random date after the given_date.
#    """
#    random_days = datetime.timedelta(days=random.randint(1, days_range))
#    return given_date + random_days

#def random_value_from_series(series):
#    """
#    Selects a random value from a given Pandas Series.
    
#    :param series: Pandas Series from which to select a random value.
#    :return: A random value from the series.
#    """
#    if series.empty:
#        return None
#    return random.choice(series.tolist())

#def generate_random_string(length):
#    """
#    Generates a random string of a specified length.

#    :param length: The desired length of the random string.
#    :return: A random string of the specified length.
#    """
#    characters = string.ascii_letters + string.digits  # Includes both letters and digits
#    return ''.join(random.choice(characters) for _ in range(length))

#def either_value_or_string(series, string_length, series_probability):
#    """
#    Returns either a random value from the series or a random string.
    
#    :param series: Pandas Series to select from.
#    :param string_length: Length of the random string to be generated.
#    :param series_probability: Probability of choosing from the series (between 0 and 1).
#    :return: Random value from series or a random string.
#    """
#    if random.random() < series_probability:
#        return random_value_from_series(series)
#    else:
#        return generate_random_string(string_length)


def random_sample(series, num_samples):
    return series.sample(n=num_samples, replace=True).tolist()

def generate_mixed_strings(series, num_strings, proportion_from_series, length_of_random_string):
    num_from_series = int(num_strings * proportion_from_series)
    num_random = num_strings - num_from_series

    # Select strings from the series
    strings_from_series = series.sample(n=num_from_series, replace=True).tolist()

    # Generate random strings
    chars = np.array(list(string.ascii_letters + string.digits))
    random_indices = np.random.randint(len(chars), size=(num_random, length_of_random_string))
    random_chars = chars[random_indices]
    random_strings = [''.join(row) for row in random_chars]

    # Combine the two sets of strings
    combined_strings = strings_from_series + random_strings

    return combined_strings


def generate_random_dates_before_range(anchor_date, num_rows, days_before):
    # Convert the anchor date to numpy datetime64
    anchor_date_np = np.datetime64(anchor_date)

    # Generate random integers within the range [0, days_before]
    random_days = np.random.randint(0, days_before, num_rows)

    # Subtract random days from the anchor date
    random_dates = anchor_date_np - np.timedelta64(1, 'D') * random_days

    return pd.Series(random_dates).dt.strftime('%Y-%m-%d')

def generate_random_dates_after_range(anchor_date, num_rows, days_after):
    # Convert the anchor date to numpy datetime64
    anchor_date_np = np.datetime64(anchor_date)

    # Generate random integers within the range [0, days_before]
    random_days = np.random.randint(0, days_after, num_rows)

    # Subtract random days from the anchor date
    random_dates = anchor_date_np + np.timedelta64(1, 'D') * random_days

    return pd.Series(random_dates).dt.strftime('%Y-%m-%d')


def create_patient_dataframe(num_rows):
    #data = {
    #    "id": [uuid.uuid4() for _ in range(num_rows)],
    #    "gender": [random_gender() for _ in range(num_rows)]
    #}

    df = pd.DataFrame()
    df["id"] = [uuid.uuid4() for _ in range(num_rows)]
    df["gender"] = rng.choice(gender_choices, size=num_rows, replace=True)
    return df
    #return pd.DataFrame(data)

def create_condition_dataframe(num_rows, vs_code, patient_ids, anchor_date):
    df = pd.DataFrame()
    df["id"] = [uuid.uuid4() for _ in range(num_rows)]
    df["code_coding_code"] = generate_mixed_strings(vs_code, num_rows, .05, 5)
    df["subject_reference"] = random_sample(patient_ids, num_rows)
    df["abatement_end"] = generate_random_dates_before_range(anchor_date, num_rows, 365)
    df["onset_end"] = generate_random_dates_after_range(anchor_date, num_rows, 365)
    df["onset_start"] = generate_random_dates_before_range(anchor_date, num_rows, 365)
    df["clinicalStatus_coding_code"] = rng.choice(active_choices, size=num_rows, replace=True)


    #data = {
    #    "id": [uuid.uuid4() for _ in range(num_rows)],
    #    "code_coding_code": [either_value_or_string(vs_code, 10, .05) for _ in range(num_rows)],
    #    "subject_reference": [random_value_from_series(patient_ids) for _ in range(num_rows)],
    #    "abatement_end": [random_date_before(anchor_date) for _ in range(num_rows)],
    #    "onset_end": [random_date_after(anchor_date) for _ in range(num_rows)],
    #    "onset_start": [random_date_before(anchor_date) for _ in range(num_rows)],
    #    "clinicalStatus_coding_code": [random_active() for _ in range(num_rows)]
    #}
    #return pd.DataFrame(data)

    return df

def create_coverage_dataframe(num_rows, patient_ids, anchor_date):
    df = pd.DataFrame()

    df["id"] = [uuid.uuid4() for _ in range(num_rows)]
    df["policyHolder_reference"] = random_sample(patient_ids, num_rows)
    df["period_end"] = generate_random_dates_after_range(anchor_date, num_rows, 180)
    df["period_start"] = generate_random_dates_before_range(anchor_date, num_rows, 180)
    df["type_coding_code"] = generate_mixed_strings(pd.Series(), num_rows, 0, 5)

    return df
    #data = {
    #    "id": [uuid.uuid4() for _ in range(num_rows)],
    #    "policyHolder_reference": [random_value_from_series(patient_ids) for _ in range(num_rows)],
    #    "period_end": [random_date_after(anchor_date, 180) for _ in range(num_rows)],
    #    "period_start": [random_date_before(anchor_date, 180) for _ in range(num_rows)],
    #    "type_coding_code": [generate_random_string(5) for _ in range(num_rows)]
    #}
    #return pd.DataFrame(data)

def create_encounter_dataframe(num_rows, vs_code, patient_ids, anchor_date):
    df = pd.DataFrame()

    df["id"] = [uuid.uuid4() for _ in range(num_rows)]
    df["type_coding_code"] = generate_mixed_strings(vs_code, num_rows, .1, 5)
    df["subject_reference"] = random_sample(patient_ids, num_rows)
    df["status"] = rng.choice(finished_choices, num_rows)
    df["period_end"] = generate_random_dates_after_range(anchor_date, num_rows, 180)
    df["period_start"] = generate_random_dates_before_range(anchor_date, num_rows, 180)

    return df


    #data = {
    #    "id": [uuid.uuid4() for _ in range(num_rows)],
    #    "type_coding_code": [either_value_or_string(vs_code, 10, .10) for _ in range(num_rows)],
    #    "subject_reference": [random_value_from_series(patient_ids) for _ in range(num_rows)],
    #    "status": [random_finished() for _ in range(num_rows)],
    #    "period_end": [random_date_after(anchor_date, 180) for _ in range(num_rows)],
    #    "period_start": [random_date_before(anchor_date, 180) for _ in range(num_rows)]
    #}
    #return pd.DataFrame(data)

def create_meds_dataframe(num_rows, vs_code, patient_ids):
    df = pd.DataFrame()

    df["id"] = [uuid.uuid4() for _ in range(num_rows)]
    df["medication"] = generate_mixed_strings(vs_code, num_rows, .1, 5)
    df["subject_reference"] = random_sample(patient_ids, num_rows)
    df["status"] = rng.choice(completed_choices, size=num_rows, replace=True)

    return df

    #data = {
    #    "id": [uuid.uuid4() for _ in range(num_rows)],
    #    "medication": [either_value_or_string(vs_code, 10, .10) for _ in range(num_rows)],
    #    "subject_reference": [random_value_from_series(patient_ids) for _ in range(num_rows)],
    #    "status": [random_completed() for _ in range(num_rows)]
    #}
    #return pd.DataFrame(data)

def create_observation_dataframe(num_rows, vs_code, patient_ids, anchor_date):
    df = pd.DataFrame()

    df["id"] = [uuid.uuid4() for _ in range(num_rows)]
    df["code_coding_code"] = generate_mixed_strings(vs_code, num_rows, .1, 5)
    df["subject_reference"] = random_sample(patient_ids, num_rows)
    df["effective_end"] = generate_random_dates_after_range(anchor_date, num_rows, 60)
    df["effective_start"] = generate_random_dates_before_range(anchor_date, num_rows, 60)

    return df

    #data = {
    #    "id": [uuid.uuid4() for _ in range(num_rows)],
    #    "code_coding_code": [either_value_or_string(vs_code, 10, .10) for _ in range(num_rows)],
    #    "subject_reference": [random_value_from_series(patient_ids) for _ in range(num_rows)],
    #    "effective_end": [random_date_after(anchor_date, 60) for _ in range(num_rows)],
    #    "effective_start": [random_date_before(anchor_date, 60) for _ in range(num_rows)]
    #}
    #return pd.DataFrame(data)

def create_procedure_dataframe(num_rows, vs_code, vs_body_code, patient_ids, anchor_date):
    df = pd.DataFrame()

    df["id"] = [uuid.uuid4() for _ in range(num_rows)]
    df["code_coding_code"] = generate_mixed_strings(vs_code, num_rows, .1, 5)
    df["bodySite_coding_code"] = generate_mixed_strings(vs_body_code, num_rows, .1, 5)
    df["subject_reference"] = random_sample(patient_ids, num_rows)
    df["status"] = rng.choice(active_choices, size=num_rows, replace=True)
    df["performed_end"] = generate_random_dates_after_range(anchor_date, num_rows, 60)
    df["performed_start"] = generate_random_dates_before_range(anchor_date, num_rows, 60)

    return df

    #data = {
    #    "id": [uuid.uuid4() for _ in range(num_rows)],
    #    "code_coding_code": [either_value_or_string(vs_code, 10, .10) for _ in range(num_rows)],
    #    "bodySite_coding_code": [either_value_or_string(vs_body_code, 10, .10) for _ in range(num_rows)],
    #    "subject_reference": [random_value_from_series(patient_ids) for _ in range(num_rows)],
    #    "status": [random_active() for _ in range(num_rows)],
    #    "performed_end": [random_date_after(anchor_date, 60) for _ in range(num_rows)],
    #    "performed_start": [random_date_before(anchor_date, 60) for _ in range(num_rows)]
    #}
    #return pd.DataFrame(data)

def make_valueset1329():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "code": "429009003",
            "version": "2021.03.20AB"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "code": "137671000119105",
            "version": "2021.03.20AB"
        },
        {
            "codesystem": "http://hl7.org/fhir/sid/icd-10-cm",
            "code": "Z90.12",
            "version": "2022.1.21AA"
        }
    ]
    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1329'
    df['id'] = 'Absence of Left Breast'
    return df
    
def make_valueset1330():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "137681000119108"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "429242008"
        },
        {
            "codesystem": "http://hl7.org/fhir/sid/icd-10-cm",
            "version": "2022.1.21AA",
            "code": "Z90.11"
        }
    ]
    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1330'
    df['id'] = 'Absence of Right Breast'
    return df

def make_valueset1042():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "456903003"
        },
        {
            "codesystem": "http://hl7.org/fhir/sid/icd-9-cm",
            "version": "2014.1.13AA",
            "code": "85.48"
        },
        {
            "codesystem": "http://hl7.org/fhir/sid/icd-9-cm",
            "version": "2014.1.13AA",
            "code": "85.44"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "27865001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "52314009"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "870629001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "14714006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "76468001"
        },
        {
            "codesystem": "http://hl7.org/fhir/sid/icd-9-cm",
            "version": "2014.1.13AA",
            "code": "85.46"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "22418005"
        },
        {
            "codesystem": "http://hl7.org/fhir/sid/icd-9-cm",
            "version": "2014.1.13AA",
            "code": "85.42"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "14693006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "60633004"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "17086001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "726636007"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "836436008"
        },
        {
            "codesystem": "https://www.cms.gov/Medicare/Coding/ICD10",
            "version": "2022.1.21AA",
            "code": "0HTV0ZZ"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1042'
    df['id'] = 'Bilateral Mastectomy'
    return df

def make_valueset1043():
    valueset_info = [
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "50"
        }
    ]
    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1043'
    df['id'] = 'Bilateral Modifier'
    return df

def make_valueset1951():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "51440002"
        }
    ]
    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1951'
    df['id'] = 'Clinical Bilateral Modifier'
    return df

def make_valueset1949():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "7771000"
        }
    ]
    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1949'
    df['id'] = 'Clinical Left Modifier'
    return df

def make_valueset1950():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "24028007"
        }
    ]
    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1950'
    df['id'] = 'Clinical Right Modifier'
    return df

def make_valueset1948():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "359740003"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "287654001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "359734005"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "66398006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "318190001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "406505007"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "395702000"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "447421006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "384723003"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "274957008"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "359728003"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "172043006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "447135002"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "446420001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "446109005"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "428564008"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "70183006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "287653007"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "237367009"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "237368004"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "359731002"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1948'
    df['id'] = 'Clinical Unilateral Mastectomy'
    return df

def make_valueset1331():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "428529004"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "136071000119101"
        },
        {
            "codesystem": "http://hl7.org/fhir/sid/icd-10-cm",
            "version": "2022.1.21AA",
            "code": "Z90.13"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1331'
    df['id'] = 'History of Bilateral Mastectomy'
    return df

def make_valueset1148():
    valueset_info = [
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "LT"
        }
    ]
    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1148'
    df['id'] = 'Left Modifier'
    return df

def make_valueset1168():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "43204002"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "833310007"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "726551006"
        },
        # ... (rest of the entries)
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "77067"
        },
        {
            "codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
            "version": "2021.3.21AA",
            "code": "G0202"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "258172002"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "12389009"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1168'
    df['id'] = 'Mammography'
    return df

def make_valueset1230():
    valueset_info = [
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "021.5.21AA",
            "code": "RT"
        }
    ]
    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1230'
    df['id'] = 'Right Modifier'
    return df

def make_valueset1256():
    valueset_info = [
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19240"
        },
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19307"
        },
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19220"
        },
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19306"
        },
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19200"
        },
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19305"
        },
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19180"
        },
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19303"
        },
        {
            "codesystem": "http://www.ama-assn.org/go/cpt",
            "version": "2021.5.21AA",
            "code": "19304"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1256'
    df['id'] = 'Unilateral Mastectomy'
    return df

def make_valueset1334():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "428571003"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "726437009"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "451211000124109"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "726429001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "741009001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "836437004"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "726435001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "741018004"
        },
        {
            "codesystem": "https://www.cms.gov/Medicare/Coding/ICD10",
            "version": "2022.1.21AA",
            "code": "0HTU0ZZ"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1334'
    df['id'] = 'Unilateral Mastectomy Left'
    return df

def make_valueset1335():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "429400009"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "726436000"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "451201000124106"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "726430006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "741010006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "836435007"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "726434002"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "741019007"
        },
        {
            "codesystem": "https://www.cms.gov/Medicare/Coding/ICD10",
            "version": "2022.1.21AA",
            "code": "0HTT0ZZ"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1335'
    df['id'] = 'Unilateral Mastectomy Right'
    return df

def make_valueset2225():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "718893008"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "718898004"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "718901003"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "718903000"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "718904006"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "718899007"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "718895001"
        },
        # ... (rest of the entries)
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "761865002"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "761866001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "457511000124100"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.2225'
    df['id'] = 'Palliative Care Assessment'
    return df

def make_valueset1450():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "305284002"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "305381007"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "713281006"
        },
        {
            "codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
            "version": "2021.3.21AA",
            "code": "G9054"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "4901000124101"
        },
        {
            "codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
            "version": "2021.3.21AA",
            "code": "M1017"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "305824005"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "305686008"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "441874000"
        },
        {
            "codesystem": "http://hl7.org/fhir/sid/icd-10-cm",
            "version": "2022.1.21AA",
            "code": "Z51.5"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1450'
    df['id'] = 'Palliative Care Encounter'
    return df

def make_valueset2224():
    valueset_info = [
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "443761007"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "433181000124107"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "103735009"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "1841000124106"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "395669003"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "395694002"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "395670002"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "395695001"
        },
        {
            "codesystem": "http://snomed.info/sct",
            "version": "2021.03.20AB",
            "code": "105402000"
        }
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.2224'
    df['id'] = 'Palliative Care Intervention'
    return df

def make_valueset1729():
    #Note: this is not the full set
    valueset_info = [
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1599805"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1602588"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1805420"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1805422"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1599803"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1602594"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1805425"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1805427"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "860695"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "860697"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "860707"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "860709"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "860715"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "860717"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996594"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996597"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996603"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996605"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996609"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996611"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996615"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996617"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "725021"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "751302"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "725023"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "725105"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1308569"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1308571"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "997220"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "997222"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "997223"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "997224"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1100184"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "1100187"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "997226"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "997228"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "997229"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "997230"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "579148"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "602734"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "310436"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "602736"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "310437"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "602737"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "860901"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996561"},
    {"codesystem": "http://www.nlm.nih.gov/research/umls/rxnorm", "version": "2021.03.01.20AB", "code": "996563"}
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1729'
    df['id'] = 'Dementia Medications'
    return df

def make_valueset1530():
    #Note: first 30 entries
    valueset_info = [
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1190"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1180"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1172"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1170"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1200"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1171"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0100"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0105"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0170"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0171"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0168"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0165"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0163"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1280"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1290"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1295"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1195"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E1285"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0465"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0466"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0304"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0302"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0250"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0251"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0290"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0291"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0303"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0301"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0270"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0260"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0261"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0294"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0295"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0265"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0266"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0296"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0297"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0255"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0256"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0292"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "E0293"}
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1530'
    df['id'] = 'Frailty Device'
    return df

def make_valueset1531():
    valueset_info = [
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "217082002"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "129588001"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "52702003"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242109009"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242391006"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242390007"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242395002"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242396001"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242389003"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "20902002"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "74541001"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "217173005"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "83468000"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "217142006"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "217086004"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242413007"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "217090002"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "217094006"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242414001"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "56307009"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "242419006"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "17886000"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "90619006"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "40104005"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "44188002"}
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1531'
    df['id'] = 'Frailty Diagnosis'
    return df

def make_valueset1532():
    valueset_info = [
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "S0311"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1022"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "G0300"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "G0299"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1021"},
        {"codesystem": "http://www.ama-assn.org/go/cpt", "version": "2021.5.21AA", "code": "99509"},
        {"codesystem": "http://www.ama-assn.org/go/cpt", "version": "2021.5.21AA", "code": "99504"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1003"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1001"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1031"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1030"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "S9124"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "S9123"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1019"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1020"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "S0271"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1000"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1005"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1002"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T1004"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "G0162"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "G0494"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "G0493"}
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1532'
    df['id'] = 'Frailty Encounter'
    return df

def make_valueset1533():
    valueset_info = [
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "162239000"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "22325002"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "431524008"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "432559006"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "267024001"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "102891000"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "67141003"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "250015009"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "13791008"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "25136009"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "248278004"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "160685001"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "127378008"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "238108007"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "788876001"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "309249007"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "284529003"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "250044006"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "365884000"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "78119002"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "160684002"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "788900007"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "79021000119104"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "429091008"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "16419651000119103"}
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1533'
    df['id'] = 'Frailty Symptom'
    return df

def make_valueset1761():
    valueset_info = [
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0115"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0125"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0135"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0145"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0155"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0235"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0650"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0651"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0652"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0655"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0656"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0657"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0658"},
        {"codesystem": "https://www.nubc.org/codesystem/RevenueCodes", "version": "2012.05", "code": "0659"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "305336008"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "183921001"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "385765002"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "Q5006"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "Q5005"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "Q5008"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "Q5007"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "Q5003"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "Q5004"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "S9126"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "T2043"}
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1761'
    df['id'] = 'Hospice Encounter'
    return df

def make_valueset1762():
    valueset_info = [
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "170935008"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "385763009"},
        {"codesystem": "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "version": "2021.3.21AA", "code": "G0182"},
        {"codesystem": "http://snomed.info/sct", "version": "2021.03.20AB", "code": "170936009"},
        {"codesystem": "http://www.ama-assn.org/go/cpt", "version": "2021.5.21AA", "code": "99377"},
        {"codesystem": "http://www.ama-assn.org/go/cpt", "version": "2021.5.21AA", "code": "99378"}
    ]

    df = pd.DataFrame(valueset_info)
    df["url"]='https://www.ncqa.org/fhir/valueset/2.16.840.1.113883.3.464.1004.1762'
    df['id'] = 'Hospice Intervention'
    return df


if len(sys.argv) > 1:
    num_rows = int(sys.argv[1])
    print(f"The argument passed is: {num_rows}")
else:
    print("No argument was passed.")

vs_1330 = make_valueset1330()
vs_1761 = make_valueset1761()
vs_1450 = make_valueset1450()
vs_1729 = make_valueset1729()
vs_1168 = make_valueset1168()
vs_1533 = make_valueset1533()
vs_1762 = make_valueset1762()
vs_1230 = make_valueset1230()

#not used in data
vs_1329 = make_valueset1329()
vs_1043 = make_valueset1043()
vs_1042 = make_valueset1042()
vs_1949 = make_valueset1949()
vs_1950 = make_valueset1950()
vs_1951 = make_valueset1951()
vs_1331 = make_valueset1331()
vs_1948 = make_valueset1948()
vs_1148 = make_valueset1148()
vs_1256 = make_valueset1256()
vs_1334 = make_valueset1334()
vs_1335 = make_valueset1335()
vs_2224 = make_valueset2224()
vs_2225 = make_valueset2225()
vs_1761 = make_valueset1761()
vs_1729 = make_valueset1729()
vs_1530 = make_valueset1530()
vs_1531 = make_valueset1531()
vs_1532 = make_valueset1532()

df_patient = create_patient_dataframe(num_rows)
df_cond = create_condition_dataframe(num_rows, vs_1330["code"], df_patient["id"], datetime.date(2022, 6, 1))
df_enc1 = create_encounter_dataframe((int)(num_rows / 2), vs_1761["code"], df_patient["id"], datetime.date(2023, 6, 1))
df_enc2 = create_encounter_dataframe((int)(num_rows / 2), vs_1450["code"], df_patient["id"], datetime.date(2023, 6, 1))
df_enc3 = create_encounter_dataframe(num_rows * 5, vs_1761["code"], df_patient["id"], datetime.date(2021, 6, 1))

df_enc = pd.concat([df_enc1, df_enc2, df_enc3], axis=0)

df_med = create_meds_dataframe(num_rows * 2, vs_1729["code"], df_patient["id"])

df_obs1 = create_observation_dataframe(num_rows, vs_1168["code"], df_patient["id"], datetime.date(2022, 1, 1))
df_obs2 = create_observation_dataframe(num_rows, vs_1533["code"], df_patient["id"], datetime.date(2022, 1, 1))
df_obs3 = create_observation_dataframe(num_rows * 2, vs_1729["code"], df_patient["id"], datetime.date(2020, 6, 1))

df_obs = pd.concat([df_obs1, df_obs2, df_obs3], axis=0)

df_proc = create_procedure_dataframe(num_rows, vs_1762["code"], vs_1230["code"], df_patient["id"], datetime.date(2022, 9, 1))
df_cov = create_coverage_dataframe(num_rows, df_patient["id"], datetime.date(2022, 6, 1))

df_vs = pd.concat([vs_1330,vs_1761,vs_1450,vs_1729,vs_1168,vs_1533,vs_1762,vs_1230,vs_1329,vs_1043,vs_1042,vs_1949,vs_1950,vs_1951,vs_1331,vs_1948,vs_1148,vs_1256,vs_1334,vs_1335,vs_2224,vs_2225,vs_1761,vs_1729,vs_1530,vs_1531,vs_1532], axis=0)

df_vs.to_csv('valuesets.csv', columns=['id', 'url', 'code', 'codesystem', 'version'], index=False)
df_patient.to_csv('patients.csv', index=False)
df_cond.to_csv('conditions.csv', index=False)
df_med.to_csv('medications.csv', index=False)
df_enc.to_csv('encounters.csv', index=False)
df_proc.to_csv('procedures.csv', index=False)
df_obs.to_csv('observations.csv', index=False)
df_cov.to_csv('coverage.csv', index=False)
