from import_codelists import cl_dict as codelists
from ehrql import create_dataset, months, case, when
from ehrql.tables.core import practice_registrations, clinical_events

dataset = create_dataset()

index_date = "2020-03-31"

has_registration = practice_registrations.for_patient_on(
    index_date
).exists_for_patient()

dataset.define_population(has_registration)

dataset.ast_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["ast_cod"]))
    .sort_by(clinical_events.date)
    .where(clinical_events.date <= index_date)
    .last_for_patient()
    .date
)

dataset.astres_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["astres_cod"]))
    .sort_by(clinical_events.date)
    .where(clinical_events.date <= index_date)
    .where(clinical_events.date < dataset.ast_dat)
    .last_for_patient()
    .date
)

dataset.asttrt_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["asttrt_cod"]))
    .sort_by(clinical_events.date)
    .where(clinical_events.date > (index_date - months(12)))
    .last_for_patient()
    .date
)

dataset.copd_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["copd_cod"]))
    .sort_by(clinical_events.date)
    .where(clinical_events.date <= index_date)
    .first_for_patient()
    .date
)

dataset.copdlat_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["copd_cod"]))
    .sort_by(clinical_events.date)
    .where(clinical_events.date <= index_date)
    .last_for_patient()
    .date
)

dataset.copdres1_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["copdres_cod"]))
    .sort_by(clinical_events.date)
    .where(clinical_events.date <= index_date)
    .where(clinical_events.date > dataset.copd_dat)
    .last_for_patient()
    .date
)

dataset.copdres_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["copdres_cod"]))
    .sort_by(clinical_events.date)
    .where(clinical_events.date <= index_date)
    .where(clinical_events.date > dataset.copdlat_dat)
    .last_for_patient()
    .date
)

dataset.copd1_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["copd_cod"]))
    .sort_by(clinical_events.date)
    .where(clinical_events.date <= index_date)
    .where(clinical_events.date > dataset.copdres1_dat)
    .last_for_patient()
    .date
)

dataset.eunrescopd_dat = case(
   when(dataset.copdres_dat.is_null() & dataset.copdres1_dat.is_null()).then(dataset.copd_dat),
   otherwise=dataset.copd1_dat,
)

dataset.saba_count = (
    clinical_events.where(clinical_events.snomedct_code.is_in(codelists["all_saba"]))
    .where(clinical_events.date > (index_date - months(12)))
    .count_for_patient()
)