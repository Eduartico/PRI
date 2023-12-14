import React, { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import MoonLoader from 'react-spinners/MoonLoader';
import { useEffect } from 'react';

// Styled components
const Container = styled.div`
  max-width: 800px;
  width: 100%;
  margin: 50px auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const Title = styled.h1`
  text-align: center;
  color: #333;
`;

const SearchContainer = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  width: 75%;
`;

const SearchInput = styled.input`
  flex: 1;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
`;

const SearchButton = styled.button`
  padding: 10px 15px;
  cursor: pointer;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 4px;
  outline: none;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #207bbf;
  }
`;

const ResultsContainer = styled.div`
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 50%;
`;


const NoResultsMessage = styled.p`
  font-style: italic;
  color: #555;
`;

const ResultItem = styled.li`
  position: relative;
  width: 100%;
  margin-bottom: 10px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: #333;

  p {
    margin: 5px 0;
  }

  .expand-button {
    cursor: pointer;
    border: none;
    background-color: transparent;
    font-size: 1.2em;
    color: #3498db;
  }
`;

const SearchResultTitle = styled.h2`
  color: #333;
`;

const FullDetailsButton = styled.button`
  margin-top: 10px;
  margin-left: 65%;
  padding: 10px 15px;
  cursor: pointer;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 4px;
  outline: none;
  display: ${(props) => (props.show ? 'block' : 'none')};
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #207bbf;
  }
`;

const ExpandButton = styled.button`
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  border: none;
  background-color: transparent;
  font-size: 1.2em;
  color: #3498db;
`;

const SearchQueryText = styled.p`
  font-style: italic;
  color: #555;
  margin-bottom: 10px;
`;

const SolrSearch = () => {
  const [query, setQuery] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const navigate = useNavigate()

  const getSearchResultsFromStorage = () => {
    const storedResults = localStorage.getItem('searchResults');
    return storedResults ? JSON.parse(storedResults) : [];
  };
  
  const setSearchResultsToStorage = (results) => {
    localStorage.setItem('searchResults', JSON.stringify(results));
  };

  const [results, setResults] = useState(getSearchResultsFromStorage());

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSearch = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:8000/search/', {
        query_text: query,
      });
      const updatedResults = response.data.results.map((result) => ({
        ...result,
        expanded: false,
      }));

      setResults(updatedResults);
      setSearchResultsToStorage(updatedResults);
      setError(null);
      setSearchQuery(query);
    } catch (error) {
      console.error('Error fetching data from Flask:', error);
      setError('An error occurred. Please try again later.');
      setTimeout(() => {
        setError(null); // Reset error state after 5 seconds
      }, 5000);
    }
    finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setResults(getSearchResultsFromStorage());
    const cachedQuery = localStorage.getItem('searchQuery');
    if (cachedQuery) {
      setSearchQuery(cachedQuery);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('searchQuery', searchQuery);
  }, [searchQuery]);

  const toggleOverview = (index) => {
    const tempResults = [...results];
    tempResults[index].expanded = !tempResults[index].expanded;
    setResults(tempResults);
  };

  const showFullDetails = (index) => {
        const selectedMovie = results[index];
        console.log(selectedMovie);
        // Use React Router to navigate to another page with the selected movie details
        navigate(`/details/`, { state: { movie: selectedMovie } });
    };

  return (
    <Container>
      <SearchQueryText>{searchQuery && `Showing results for: ${searchQuery}`}</SearchQueryText>
      <Title>FEUPFLIX</Title>

      <SearchContainer>
        <SearchInput type="text" value={query} onChange={handleInputChange} placeholder="Enter your search query" />
        <SearchButton onClick={handleSearch}>Search</SearchButton>
      </SearchContainer>

      <ResultsContainer>
        <SearchResultTitle>Search Results</SearchResultTitle>
        
        { loading ? (
          <MoonLoader
          color="#333"
          size={60}
          speedMultiplier={1}
          loading={loading}
        />
        ) : error ? (
          <NoResultsMessage>{error}</NoResultsMessage>
        ) : results.length > 0 && !(searchQuery === '') ? (
          <ul style={{ listStyle: 'none', padding: '0', width: '100%' }}>
          {results.map((result, index) => (
            <ResultItem key={index}>
              <ExpandButton onClick={() => toggleOverview(index)}>
                  {result.expanded ? '-' : '+'}
                </ExpandButton>
              <p><strong>Title:</strong> {result.movie_title}</p>
              <p><strong>Score:</strong> {result.score * 100}</p>
              {result.expanded && (
                <p>
                  <strong>Overview:</strong> {result.Overview}
                </p>
              )}
              <FullDetailsButton show={result.expanded} onClick={() => showFullDetails(index)}>
                  Show Full Details
              </FullDetailsButton>
            </ResultItem>
          ))}
        </ul>
        ) : (
          <NoResultsMessage>No results found.</NoResultsMessage>
        )}
      </ResultsContainer>
    </Container>
  );
};

export default SolrSearch;
