// @generated automatically by Diesel CLI.

diesel::table! {
    vacancies (pk) {
        pk -> Int4,
        uid -> Varchar,
        company -> Varchar,
        position -> Varchar,
        location -> Varchar,
        contract -> Varchar,
        remote -> Varchar,
        salary_min -> Nullable<Int4>,
        salary_max -> Nullable<Int4>,
        about -> Text,
        requirements -> Text,
        responsibilities -> Text,
    }
}
