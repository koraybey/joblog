// @generated automatically by Diesel CLI.

diesel::table! {
    vacancies (pk) {
        pk -> Int4,
        uid -> Varchar,
        company_logo -> Varchar,
        company -> Varchar,
        title -> Varchar,
        description -> Text,
        experience_level -> Varchar,
        contract_type -> Varchar,
        location -> Varchar,
        workplace_type -> Varchar,
        company_url -> Varchar,
        date_created -> Nullable<Timestamp>,
        date_modified -> Nullable<Timestamp>,
    }
}
