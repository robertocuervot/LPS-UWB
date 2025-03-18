using System;
using UnityEngine;
using System.IO.Ports;

public class Positionball : MonoBehaviour
{
    // Définition des ancres avec leurs positions fixes
    private Vector3 Ancre1 = new Vector3(0f, 0f, 2f);  // Coin bas gauche (Hauteur = 2m)
    private Vector3 Ancre2 = new Vector3(16f, 0f, 2f); // Coin bas droit
    private Vector3 Ancre3 = new Vector3(0f, 8f, 2f);  // Coin haut gauche
    private Vector3 Ancre4 = new Vector3(16f, 8f, 2f); // Coin haut droit

    // Distances mesurées (reçues d’Arduino)
    private float d1, d2, d3, d4;

    // Référence vers l’objet représentant le tag dans Unity
    public GameObject tagObject;

    // Configuration du port série pour recevoir les données d'Arduino
    private SerialPort serialPort = new SerialPort("COM3", 115200);

    void Start()
    {
        // Ouvre la connexion série avec Arduino
        if (!serialPort.IsOpen)
        {
            serialPort.Open();
            serialPort.ReadTimeout = 100;
        }
    }

    void Update()
    {
        // Lecture des données depuis Arduino
        ReadSerialData();

        // Calcul de la position du tag
        Vector3 tagPosition = Trilateration(Ancre1, d1, Ancre2, d2, Ancre3, d3);

        // Mise à jour de la position de l’objet tag dans Unity
        tagObject.transform.position = tagPosition;
    }

    void ReadSerialData()
    {
        try
        {
            if (serialPort.IsOpen)
            {
                string data = serialPort.ReadLine(); // Exemple : "5.2, 7.4, 6.1, 7.8"
                string[] values = data.Split(',');

                if (values.Length == 4)
                {
                    d1 = float.Parse(values[0]);
                    d2 = float.Parse(values[1]);
                    d3 = float.Parse(values[2]);
                    d4 = float.Parse(values[3]);
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogWarning("Erreur lecture port série : " + e.Message);
        }
    }

    Vector3 Trilateration(Vector3 a1, float r1, Vector3 a2, float r2, Vector3 a3, float r3)
    {
        float A = 2 * (a2.x - a1.x);
        float B = 2 * (a2.y - a1.y);
        float C = 2 * (a3.x - a1.x);
        float D = 2 * (a3.y - a1.y);

        float E = Mathf.Pow(r1, 2) - Mathf.Pow(r2, 2) - Mathf.Pow(a1.x, 2) + Mathf.Pow(a2.x, 2) - Mathf.Pow(a1.y, 2) + Mathf.Pow(a2.y, 2);
        float F = Mathf.Pow(r1, 2) - Mathf.Pow(r3, 2) - Mathf.Pow(a1.x, 2) + Mathf.Pow(a3.x, 2) - Mathf.Pow(a1.y, 2) + Mathf.Pow(a3.y, 2);

        float x = (E * D - B * F) / (A * D - B * C);
        float y = (A * F - C * E) / (A * D - B * C);
        float z = (a1.z + a2.z + a3.z) / 3; // Hauteur approximative

        return new Vector3(x, y, z);
    }

    void OnApplicationQuit()
    {
        if (serialPort.IsOpen)
        {
            serialPort.Close();
        }
    }
}
