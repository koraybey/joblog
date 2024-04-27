use super::schema::vacancies;
use juniper::GraphQLInputObject;
use serde::Deserialize;

#[derive(Queryable, juniper::GraphQLObject)]
#[diesel(table_name = vacancies)]

pub struct Vacancy {
    #[graphql(skip)]
    pub pk: i32,
    pub uid: String,
    pub company_logo: String,
    pub company: String,
    pub title: String,
    pub description: String,
    pub location: String,
    pub workplace_type: Option<String>, // On-site, Hybrid, Remote
    pub url: String,
    pub company_url: String,
    pub date_created: Option<chrono::NaiveDateTime>,
    pub date_modified: Option<chrono::NaiveDateTime>,
    pub experience_level: Option<String>, // Internship, Entry, Associate, Mid-Senior, Director, Executive
    pub contract_type: Option<String>,    // Full-time, Part-time, Contract, Internship
    pub status: Option<String>,
}




#[derive(GraphQLInputObject, AsChangeset)]
#[diesel(table_name = vacancies)]
pub struct VacancyInput {
    pub company_logo: String,
    pub company: String,
    pub title: String,
    pub description: String,
    pub location: String,
    pub workplace_type: Option<String>, // On-site, Hybrid, Remote
    pub url: String,
    pub company_url: String,
    pub experience_level: Option<String>, // Internship, Entry, Associate, Mid-Senior, Director, Executive
    pub contract_type: Option<String>,    // Full-time, Part-time, Contract, Internship
    pub status: Option<String>,
}


#[derive(Insertable, Deserialize, AsChangeset)]
#[diesel(table_name = vacancies)]
pub struct NewVacancy {
    pub uid: String,
    pub company_logo: String,
    pub company: String,
    pub title: String,
    pub description: String,
    pub location: String,
    pub workplace_type: Option<String>, // On-site, Hybrid, Remote
    pub url: String,
    pub company_url: String,
    pub experience_level: Option<String>, // Internship, Entry, Associate, Mid-Senior, Director, Executive
    pub contract_type: Option<String>,    // Full-time, Part-time, Contract, Internship
    pub status: Option<String>,
}

#[derive(GraphQLInputObject, Insertable, Deserialize, AsChangeset)]
#[diesel(table_name = vacancies)]
pub struct VacancyMutation {
    pub uid: String,
    pub status: Option<String>,
}
