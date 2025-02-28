import { useState } from "react";
import { Input } from "./components/ui/input";
import { Button } from "./components/ui/button";
import { Signup } from "./components/signup";
import { Login } from "./components/login";
import { useMutation, useQuery } from "@apollo/client";
import {
  CHECK_AUTH_QUERY,
  CREATE_PORTFOLIO_MUTATION,
  GET_PORTFOLIOS_QUERY,
} from "./lib/apollo";
import { Logout } from "./components/ui/logout";

function App() {
  const {
    data: portfolios,
    loading,
    error,
    refetch: refetchPortfolios,
  } = useQuery(GET_PORTFOLIOS_QUERY);
  const res = useQuery(CHECK_AUTH_QUERY);
  const [createPortfolioMutation, { loading: createPortfolioLoadin }] =
    useMutation(CREATE_PORTFOLIO_MUTATION);

  const [jobsCount, setJobsCount] = useState();
  const [roleName, setRoleName] = useState("");

  const handleSubmit = async () => {
    if (!jobsCount || !roleName.length) return;
    const { data, errors, extensions } = await createPortfolioMutation({
      variables: { roleName, jobsCount: parseInt(jobsCount) },
    });
    refetchPortfolios();
  };

  return (
    <div className="flex flex-col justify-center items-center h-screen gap-6">
      <Logout />
      <Signup />
      <Login />
      <div className="border border-border w-1/2 h-1/2 flex flex-col gap-3 p-4">
        <Input
          value={jobsCount}
          onChange={(e) => setJobsCount(e.target.value)}
          placeholder="job count..."
        />
        <Input
          value={roleName}
          onChange={(e) => setRoleName(e.target.value)}
          placeholder="job title"
        />
        <Button onClick={handleSubmit}>Submit</Button>

        <div className="flex flex-col border border-border h-full p-2 overflow-hidden">
          <div className="flex-1 overflow-auto">
            {JSON.stringify(portfolios)}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
