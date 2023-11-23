/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   win_rate.js                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:24:57 by lflandri          #+#    #+#             */
/*   Updated: 2023/11/23 15:29:06 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//TODO all

function win_rate_calcul(win_rate) {
	document.getElementById("progg_bar_win_rate").style.width = "" +  (win_rate * 100) +  "%"; 
}

win_rate_calcul(0.30);