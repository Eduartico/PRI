import React from 'react';
import { useLocation } from 'react-router-dom';
import styled from 'styled-components';

// Styled components
const DetailsContainer = styled.div`
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
  color: #333;
`;

const Title = styled.h1`
  text-align: center;
  color: #333;
`;

const DetailSection = styled.div`
  margin: 20px 0;
    width: 90%;
`;

const DetailTitle = styled.h2`
  color: #3498db;
`;

const DetailItem = styled.p`
  margin: 10px 0;
`;

const PosterDiv = styled.div`
  width: 50%;
  display: flex;
  justify-content: center;
`;

const StyledPosterImage = styled.img`
  width: 100%;
  max-width: 300px;
  max-height: 450px;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 3); 
  object-fit: cover;
`;

const MovieDetails = () => {
  const location = useLocation();
  const movie = location.state?.movie;

  if (!movie) {
    return <div>No movie details available.</div>;
  }

  return (
    <DetailsContainer>
      <Title>{movie.movie_title}</Title>
      {movie.Poster_Image && (
        <PosterDiv>
          <StyledPosterImage src={movie.Poster_Image} alt="Movie Poster" />
        </PosterDiv>
      )}
      <DetailSection>
        <DetailTitle>Overview</DetailTitle>
        <DetailItem>{movie.Overview || 'No overview available.'}</DetailItem>
      </DetailSection>

      <DetailSection>
        <DetailTitle>Details</DetailTitle>
        <DetailItem>
          <strong>Rating:</strong> {movie.Rating || 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>User Rating:</strong> {movie.User_rating || 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>Genres:</strong> {movie.Generes ? movie.Generes.join(', ') : 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>Director:</strong> {movie.Director || 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>Writer:</strong> {movie.Writer ? movie.Writer.join(', ') : 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>Year:</strong> {movie.year || 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>Popularity:</strong> {movie.Popularity || 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>Votes:</strong> {movie.Votes || 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>Adult:</strong> {movie.Adult ? 'Yes' : 'No'}
        </DetailItem>
        <DetailItem>
          <strong>Runtime:</strong> {movie.Runtime ? `${movie.Runtime} minutes` : 'N/A'}
        </DetailItem>
        <DetailItem>
          <strong>Taglines:</strong> {movie.Taglines ? movie.Taglines.join(', ') : 'N/A'}
        </DetailItem>
      </DetailSection>

      <DetailSection>
        <DetailTitle>Top 5 Casts</DetailTitle>
        <DetailItem>{movie.Top_5_Casts ? movie.Top_5_Casts.join(', ') : 'N/A'}</DetailItem>
      </DetailSection>

    </DetailsContainer>
  );
};


export default MovieDetails;
