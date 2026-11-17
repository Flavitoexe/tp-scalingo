import { useParams, useLoaderData } from "react-router"
import { useState, useEffect } from "react"

type Data = {
    title: string,
    content: string
}

export default function Article() {


    const data = useLoaderData() as Data

    return (
        data != null && (
            <article>
                <h1>{data.title}</h1>
                <p>{data.content}</p>
            </article>
        )
    )
}