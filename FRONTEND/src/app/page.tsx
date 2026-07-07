import { Box, Stack, Typography } from "@mui/material";


export default function Home() {
  return (

       <Stack sx={{  alignItems: "center", flex: 1, justifyContent: "center"}}>
       <Typography variant="h3">NoteBookLM Clone</Typography>
       <Typography variant="h5">Transform your documents into a private AI-powered knowledge base.</Typography>
       <Stack direction="row">
        <Box>a</Box>
        <Box>a</Box>
       </Stack>
       </Stack> 
  );
}
