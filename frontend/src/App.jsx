import Earthquakes from './Earthquakes';
import { Analytics } from '@vercel/analytics/react';

function App() {
  return (
    <>
      <Earthquakes />
      <Analytics />
    </>
  );
}

export default App;