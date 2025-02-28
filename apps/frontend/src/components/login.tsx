import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useState } from "react";
import { useMutation } from "@apollo/client";
import { LOGIN_MUTATION } from "@/lib/apollo";

export const Login = () => {
  const [loginMutation] = useMutation(LOGIN_MUTATION);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async () => {
    const {data, errors, extensions} = await loginMutation({
      variables: { username, password },
    });
  };

  return (
    <div className="border border-border w-1/2 flex flex-col gap-3 p-4">
      <Input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="username"
      />
      <Input
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="password"
      />
      <Button onClick={handleSubmit}>Login</Button>
    </div>
  );
};
