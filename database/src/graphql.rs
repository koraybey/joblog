use super::context::GraphQLContext;
use diesel::pg::PgConnection;
use juniper::{graphql_object, EmptySubscription, FieldResult};

use super::data::Vacancies;
use super::models::{Vacancy, VacancyInput};

// The root GraphQL query
pub struct Query;

// The root Query struct relies on GraphQLContext to provide the connection pool
// needed to execute actual Postgres queries.
#[graphql_object(Context = GraphQLContext)]
impl Query {
    #[graphql(name = "allVacancies")]
    pub fn all_vacancies(context: &GraphQLContext) -> FieldResult<Vec<Vacancy>> {
        // TODO: pass the GraphQLContext into the querying functions rather
        // than a PgConnection (for brevity's sake)
        let conn: &PgConnection = &context.pool.get().unwrap();
        Vacancies::all_vacancies(conn)
    }
    #[graphql(name = "getVacancyByUid")]
    pub fn get_vacancy_by_uid(
        context: &GraphQLContext,
        uid: String,
    ) -> FieldResult<Option<Vacancy>> {
        let conn: &PgConnection = &context.pool.get().unwrap();
        Vacancies::get_vacancy_by_id(conn, uid)
    }
}

// The root GraphQL mutation
pub struct Mutation;

#[graphql_object(Context = GraphQLContext)]
impl Mutation {
    #[graphql(name = "createVacancy")]
    pub fn create_vacancy(
        context: &GraphQLContext,
        input: VacancyInput,
    ) -> FieldResult<Vacancy> {
        let conn: &PgConnection = &context.pool.get().unwrap();
        Vacancies::create_vacancy(conn, input)
    }
    #[graphql(name = "deleteVacancy")]
    pub fn delete_vacancy(context: &GraphQLContext, id: String) -> FieldResult<bool> {
        let conn: &PgConnection = &context.pool.get().unwrap();
        Vacancies::delete_vacancy(conn, id)
    }
}

pub type Schema =
    juniper::RootNode<'static, Query, Mutation, EmptySubscription<GraphQLContext>>;

pub fn create_schema() -> Schema {
    Schema::new(Query, Mutation, EmptySubscription::new())
}
