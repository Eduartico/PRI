import React from 'react';
import './App.css';
import styled from 'styled-components';
import SolrSearch from './SolrSearch.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MovieDetails from './MovieDetails.js';

// Styled components
const AppContainer = styled.div`
  background: linear-gradient(to right, #3498db, #2c3e50);
  color: #fff;
  min-height: 100vh;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Header = styled.header`
  margin-bottom: 30px;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: left;
  justify-content: left;
  gap: 70px;
  margin-top: 30px;
  margin-left: 60px;
`;

const Logo = styled.img`
  width: 200px;
`;

const App = () => {
  return (
    <AppContainer>
      <Header>
        <Logo src={"/feup-logo.png"} alt="Logo" />
      </Header>
      <Router>
        <Routes>
          <Route path="/" exact element={<SolrSearch />} />
          <Route path="/details/" element={<MovieDetails/>} />
        </Routes>
      </Router>
    </AppContainer>
  );
};

export default App;
