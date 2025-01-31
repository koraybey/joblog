use super::models::{NewVacancy, Vacancy, VacancyInput};
use super::schema::vacancies::dsl::*;
use diesel::pg::PgConnection;
use diesel::prelude::*;
use juniper::{FieldError, FieldResult};
use uuid::Uuid;
// This struct is basically a query manager. All the methods that it
// provides are static, making it a convenient abstraction for interacting
// with the database.
pub struct Vacancies;

// Note that all the function names here map directly onto the function names
// associated with the Query and Mutation structs. This is NOT necessary but
// I personally prefer it.
impl Vacancies {
    pub fn all_vacancies(conn: &PgConnection) -> FieldResult<Vec<Vacancy>> {
        let res = vacancies.order(date_created.desc()).load::<Vacancy>(conn);
        graphql_translate(res)
    }

    pub fn create_vacancy(
        conn: &PgConnection,
        new_vacancy: VacancyInput,
    ) -> FieldResult<Vacancy> {
        use super::schema::vacancies;
        let uid_ = Uuid::new_v4().to_string();

        let new_vacancy = NewVacancy {
            uid: &uid_,
            company: &new_vacancy.company,
            company_logo: &new_vacancy.company_logo,
            title: &new_vacancy.title,
            description: &new_vacancy.description,
            experience_level: new_vacancy.experience_level,
            contract_type: new_vacancy.contract_type,
            location: &new_vacancy.location,
            workplace_type: new_vacancy.workplace_type,
            url: &new_vacancy.url,
            company_url: &new_vacancy.company_url,
        };

        let res = diesel::insert_into(vacancies::table)
            .values(&new_vacancy)
            .get_result(conn);

        graphql_translate(res)
    }

    pub fn delete_vacancy(conn: &PgConnection, uid_: String) -> FieldResult<bool> {
        let old_count = vacancies.count().first::<i64>(conn);
        match diesel::delete(vacancies.filter(uid.eq(uid_))).execute(conn) {
            Ok(_) => {
                if vacancies.count().first(conn) == old_count.map(|count| count - 1) {
                    Ok(true)
                } else {
                    Ok(false)
                }
            }
            Err(e) => match e {
                // Without this translation, GraphQL will return an error rather
                // than the more semantically sound JSON null if no TODO is found.
                diesel::result::Error::NotFound => FieldResult::Ok(false),
                _ => FieldResult::Err(FieldError::from(e)),
            },
        }
    }

    pub fn get_vacancy(
        conn: &PgConnection,
        uid_: String,
    ) -> FieldResult<Option<Vacancy>> {
        match vacancies.filter(uid.eq(uid_)).get_result(conn) {
            Ok(vacancy) => Ok(Some(vacancy)),
            Err(e) => match e {
                // Without this translation, GraphQL will return an error rather
                // than the more semantically sound JSON null if no TODO is found.
                diesel::result::Error::NotFound => FieldResult::Ok(None),
                _ => FieldResult::Err(FieldError::from(e)),
            },
        }
    }
}

fn graphql_translate<T>(res: Result<T, diesel::result::Error>) -> FieldResult<T> {
    match res {
        Ok(t) => Ok(t),
        Err(e) => FieldResult::Err(FieldError::from(e)),
    }
}
