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
        let res = vacancies.load::<Vacancy>(conn);
        graphql_translate(res)
    }

    pub fn create_vacancy(
        conn: &PgConnection,
        new_vacancy: VacancyInput,
    ) -> FieldResult<Vacancy> {
        use super::schema::vacancies;
        let id = Uuid::new_v4().to_string();

        let new_vacancy = NewVacancy {
            uid: &id,
            company: &new_vacancy.company,
            position: &new_vacancy.position,
            location: &new_vacancy.location,
            contract: &new_vacancy.contract,
            remote: &new_vacancy.remote,
            salary_min: new_vacancy.salary_min,
            salary_max: new_vacancy.salary_max,
            about: &new_vacancy.about,
            requirements: &new_vacancy.requirements,
            responsibilities: &new_vacancy.responsibilities,
        };

        let res = diesel::insert_into(vacancies::table)
            .values(&new_vacancy)
            .get_result(conn);

        graphql_translate(res)
    }

    pub fn delete_vacancy(conn: &PgConnection, vacancy_id: String) -> FieldResult<bool> {
        let old_count = vacancies.count().first::<i64>(conn);
        match diesel::delete(vacancies.filter(uid.eq(vacancy_id))).execute(conn) {
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

    pub fn get_vacancy_by_id(
        conn: &PgConnection,
        id: String,
    ) -> FieldResult<Option<Vacancy>> {
        match vacancies.filter(uid.eq(id)).get_result(conn) {
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
