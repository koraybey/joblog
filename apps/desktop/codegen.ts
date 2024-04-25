import type { CodegenConfig } from '@graphql-codegen/cli'

declare module "bun" {
    interface Env {
        GRAPHQL_ENDPOINT: string;
    }
  }
  
const config: CodegenConfig = {
    overwrite: true,
    schema: process.env.GRAPHQL_ENDPOINT,
    generates: {
        'src/__generated__/gql/': {
            preset: 'client',
            plugins: [],
        },
    },
}

export default config
