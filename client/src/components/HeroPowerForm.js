import { useEffect, useState } from "react";
import { useHistory } from "react-router";

function HeroPowerForm() {
  const [heroes, setHeroes] = useState([]);
  const [powers, setPowers] = useState([]);
  const [heroId, setHeroId] = useState("");
  const [powerId, setPowerId] = useState("");
  const [strength, setStrength] = useState("");
  const [formErrors, setFormErrors] = useState([]);
  const history = useHistory();

  useEffect(() => {
    fetch("/heroes")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch heroes");
        }
        return response.json();
      })
      .then(setHeroes)
      .catch((error) => console.error(error));
  }, []);

  useEffect(() => {
    fetch("/powers")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch powers");
        }
        return response.json();
      })
      .then(setPowers)
      .catch((error) => console.error(error));
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    const formData = {
      hero_id: heroId,
      power_id: powerId,
      strength: strength,
    };
    fetch("/hero_powers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (response.ok) {
          history.push(`/heroes/${heroId}`);
        } else {
          return response.json().then((data) => {
            if (Array.isArray(data.errors)) {
              setFormErrors(data.errors);
            } else {
              setFormErrors(["An unknown error occurred"]);
            }
            throw new Error("Failed to add hero power");
          });
        }
      })
      .catch((error) => console.error(error));
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="power_id">Power:</label>
      <select
        id="power_id"
        name="power_id"
        value={powerId}
        onChange={(e) => setPowerId(e.target.value)}
      >
        <option value="">Select a power</option>
        {powers.map((power) => (
          <option key={power.id} value={power.id}>
            {power.name}
          </option>
        ))}
      </select>
      <label htmlFor="hero_id">Hero:</label>
      <select
        id="hero_id"
        name="hero_id"
        value={heroId}
        onChange={(e) => setHeroId(e.target.value)}
      >
        <option value="">Select a hero</option>
        {heroes.map((hero) => (
          <option key={hero.id} value={hero.id}>
            {hero.name}
          </option>
        ))}
      </select>
      <label htmlFor="strength">Strength:</label>
      <input
        type="text"
        id="strength"
        name="strength"
        value={strength}
        onChange={(e) => setStrength(e.target.value)}
      />
      {formErrors.length > 0 &&
        formErrors.map((err, index) => (
          <p key={index} style={{ color: "red" }}>
            {err}
          </p>
        ))}
      <button type="submit">Add Hero Power</button>
    </form>
  );
}

export default HeroPowerForm;
