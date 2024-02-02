use super::schema::vacancies;
use juniper::GraphQLInputObject;

// The core data type undergirding the GraphQL interface
#[derive(Queryable, juniper::GraphQLObject)]
pub struct Vacancy {
    pk: i32,
    pub uid: String,
    pub company: String,
    pub position: String,
    pub location: String,
    pub contract: String,
    pub remote: String,
    pub salary_min: Option<i32>,
    pub salary_max: Option<i32>,
    pub about: String,
    pub requirements: String,
    pub responsibilities: String,
}
#[derive(Insertable)]
#[table_name = "vacancies"]
pub struct NewVacancy<'a> {
    pub uid: &'a String,
    pub company: &'a String,
    pub position: &'a String,
    pub location: &'a String,
    pub contract: &'a String,
    pub remote: &'a String,
    pub salary_min: Option<i32>,
    pub salary_max: Option<i32>,
    pub about: &'a String,
    pub requirements: &'a String,
    pub responsibilities: &'a String,
}

#[derive(GraphQLInputObject)]
pub struct VacancyInput {
    pub company: String,
    pub position: String,
    pub location: String,
    pub contract: String,
    pub remote: String,
    pub salary_min: Option<i32>,
    pub salary_max: Option<i32>,
    pub about: String,
    pub requirements: String,
    pub responsibilities: String,
}
