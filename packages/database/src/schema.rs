// @generated automatically by Diesel CLI.

diesel::table! {
    vacancies (pk) {
        pk -> Int4,
        uid -> Varchar,
        company_logo -> Varchar,
        company -> Varchar,
        title -> Varchar,
        description -> Text,
        location -> Varchar,
        workplace_type -> Nullable<Varchar>,
        url -> Varchar,
        company_url -> Varchar,
        date_created -> Nullable<Timestamp>,
        date_modified -> Nullable<Timestamp>,
        experience_level -> Nullable<Varchar>,
        contract_type -> Nullable<Varchar>,
    }
}
