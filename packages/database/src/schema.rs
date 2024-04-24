// @generated automatically by Diesel CLI.

diesel::table! {
    analyses (pk) {
        pk -> Int4,
        uid -> Varchar,
        company -> Varchar,
        title -> Varchar,
        #[sql_name = "match"]
        match_ -> Varchar,
        relevance -> Varchar,
        reason -> Nullable<Text>,
        date_created -> Nullable<Timestamp>,
        date_modified -> Nullable<Timestamp>,
    }
}

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

diesel::allow_tables_to_appear_in_same_query!(analyses, vacancies,);
