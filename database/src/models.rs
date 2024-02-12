use super::schema::vacancies;
use juniper::GraphQLInputObject;

#[derive(Queryable, juniper::GraphQLObject)]
pub struct Vacancy {
    #[graphql(skip)]
    pub pk: i32,
    pub uid: String,
    pub company_logo: String,
    pub company: String,
    pub title: String,
    pub description: String,
    pub experience_level: String,  // Internship, Entry, Associate, Mid-Senior, Director, Executive
    pub contract_type: String,   // Full-time, Part-time, Contract, Internship
    pub location: String,
    pub workplace_type: String,  // On-site, Hybrid, Remote
    pub company_url: String,    
    pub date_created: Option<chrono::NaiveDateTime>,
    pub date_modified: Option<chrono::NaiveDateTime>,

}

#[derive(Insertable)]
#[table_name = "vacancies"]
pub struct NewVacancy<'a> {
    pub uid: &'a String,
    pub company_logo: &'a String,
    pub company: &'a String,
    pub title: &'a String,
    pub description: &'a String,
    pub experience_level: &'a String,  // Internship, Entry, Associate, Mid-Senior, Director, Executive
    pub contract_type: &'a String,   // Full-time, Part-time, Contract, Internship
    pub location: &'a String,
    pub workplace_type: &'a String,  // On-site, Hybrid, Remote
    pub company_url: &'a String,
}

#[derive(GraphQLInputObject)]
pub struct VacancyInput {
    pub company_logo: String,
    pub company: String,
    pub title: String,
    pub description: String,
    pub experience_level: String,  // Internship, Entry, Associate, Mid-Senior, Director, Executive
    pub contract_type: String,   // Full-time, Part-time, Contract, Internship
    pub location: String,
    pub workplace_type: String,  // On-site, Hybrid, Remote
    pub company_url: String,    
}
