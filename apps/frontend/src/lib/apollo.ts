import { gql } from "@apollo/client";

export const SIGNUP_MUTATION = gql`
  mutation Signup($username: String!, $password: String!) {
    signup(userData: { username: $username, password: $password }) {
      success
      message
      user {
        id
        username
      }
    }
  }
`;

export const LOGIN_MUTATION = gql`
  mutation Login($username: String!, $password: String!) {
    login(loginData: { username: $username, password: $password }) {
      success
      message
      user {
        id
        username
      }
    }
  }
`;

export const CREATE_PORTFOLIO_MUTATION = gql`
  mutation createPortfolio($roleName: String!, $jobsCount: Int!) {
    createPortfolio(
      portfolioData: { roleName: $roleName, jobsCount: $jobsCount }
    ) {
      id
      roleName
      jobsCount
      createdAt
    }
  }
`;

export const GET_PORTFOLIOS_QUERY = gql`
  query {
    getPortfolios {
      id
      roleName
      jobsCount
      createdAt
    }
  }
`;

export const CHECK_AUTH_QUERY = gql`
  query {
    checkAuth {
      success
      message
      user {
        id
        username
      }
    }
  }
`;

export const LOGOUT_MUTATION = gql`
  mutation {
    logout {
      success
      message
    }
  }
`;
