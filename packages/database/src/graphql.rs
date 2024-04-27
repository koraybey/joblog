use super::context::GraphQLContext;
use diesel::pg::PgConnection;
use juniper::{graphql_object, EmptySubscription, FieldResult};

use super::data::Vacancies;
use super::models::{Vacancy, VacancyInput, VacancyMutation};

pub struct Query;
#[graphql_object(Context = GraphQLContext)]
impl Query {

    pub fn all_vacancies(context: &GraphQLContext) -> FieldResult<Vec<Vacancy>> {
        let conn: &mut PgConnection = &mut context.pool.get().unwrap();
        Vacancies::all_vacancies(conn)
    }

    pub fn get_vacancy(
        context: &GraphQLContext,
        uid: String,
    ) -> FieldResult<Option<Vacancy>> {
        let conn: &mut PgConnection = &mut context.pool.get().unwrap();
        Vacancies::get_vacancy(conn, uid)
    }
}

// The root GraphQL mutation
pub struct Mutation;

#[graphql_object(Context = GraphQLContext)]
impl Mutation {
    pub fn create_vacancy(
        context: &GraphQLContext,
        input: VacancyInput,
    ) -> FieldResult<Vacancy> {
        let conn: &mut PgConnection = &mut context.pool.get().unwrap();
        Vacancies::create_vacancy(conn, input)
    }

    pub fn delete_vacancy(context: &GraphQLContext, uid: String) -> FieldResult<bool> {
        let conn: &mut PgConnection = &mut context.pool.get().unwrap();
        Vacancies::delete_vacancy(conn, uid)
    }

    pub fn update_vacancy(
        context: &GraphQLContext,
        input: VacancyMutation,
    ) -> FieldResult<Vacancy> {
        let conn: &mut PgConnection = &mut context.pool.get().unwrap();
        Vacancies::update_vacancy(conn, input)
    }
}

pub type Schema =
    juniper::RootNode<'static, Query, Mutation, EmptySubscription<GraphQLContext>>;

pub fn create_schema() -> Schema {
    Schema::new(Query, Mutation, EmptySubscription::new())
}
