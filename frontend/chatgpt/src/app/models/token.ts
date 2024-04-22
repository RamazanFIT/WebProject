// auth-token.model.ts
export interface AuthToken {
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
  };
}

